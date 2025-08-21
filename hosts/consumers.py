import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Device
from .choices import DeviceStatusChoice


class AgentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.bios_uuid = self.scope['url_route']['kwargs']['bios_uuid']
        self.group_name = f'device_{self.bios_uuid}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Device ni online qilish
        device_updated = await self.set_online()
        if device_updated:
            # Barcha mijozlarga device status o'zgarganini xabar berish
            await self.broadcast_device_status()
            print(f"✅ Device {self.bios_uuid} is now ONLINE")

    async def disconnect(self, close_code):
        # Device ni offline qilish
        device_updated = await self.set_offline()
        if device_updated:
            # Barcha mijozlarga device status o'zgarganini xabar berish
            await self.broadcast_device_status()
            print(f"❌ Device {self.bios_uuid} is now OFFLINE")

        # Group dan chiqarish
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """Agent dan kelgan xabarlarni qabul qilish"""
        try:
            data = json.loads(text_data)
            print(f"📨 Received from {self.bios_uuid}: {data}")

            # Agent dan kelgan ma'lumotlarni boshqa mijozlarga yuborish mumkin
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'agent_message',
                    'message': data
                }
            )
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON from {self.bios_uuid}: {text_data}")

    async def agent_message(self, event):
        """Agent dan kelgan xabarni mijozlarga yuborish"""
        await self.send(text_data=json.dumps({
            'type': 'agent_data',
            'data': event['message']
        }))

    @database_sync_to_async
    def set_online(self):
        """Device ni online qilish"""
        try:
            device = Device.objects.get(bios_uuid=self.bios_uuid)
            device.status = DeviceStatusChoice.Online
            device.save(update_fields=['status'])
            return True
        except Device.DoesNotExist:
            print(f"❌ Device with UUID {self.bios_uuid} not found in database")
            return False

    @database_sync_to_async
    def set_offline(self):
        """Device ni offline qilish"""
        try:
            device = Device.objects.get(bios_uuid=self.bios_uuid)
            device.status = DeviceStatusChoice.Offline
            device.last_seen = timezone.now()
            device.save(update_fields=['status', 'last_seen'])
            return True
        except Device.DoesNotExist:
            print(f"❌ Device with UUID {self.bios_uuid} not found in database")
            return False

    @database_sync_to_async
    def get_device_status(self):
        """Device ning hozirgi holatini olish"""
        try:
            device = Device.objects.get(bios_uuid=self.bios_uuid)
            return {
                'bios_uuid': str(device.bios_uuid),  # UUID ni string ga aylantirish
                'status': device.status,
                'last_seen': device.last_seen.isoformat() if device.last_seen else None,
                'name': getattr(device, 'name', None),  # Agar name maydoni bo'lsa
            }
        except Device.DoesNotExist:
            return None

    async def broadcast_device_status(self):
        """
        Device status o'zgarganini barcha DevicesListConsumer larga xabar berish
        """
        device_data = await self.get_device_status()
        if device_data:
            # Barcha devices list consumerlariga xabar yuborish
            await self.channel_layer.group_send(
                "devices_list",  # DevicesListConsumer group nomi
                {
                    'type': 'device_status_update',
                    'device_data': device_data
                }
            )


class DevicesListConsumer(AsyncWebsocketConsumer):
    """
    Barcha devicelar ro'yxatini real-time da ko'rsatish uchun consumer
    """

    async def connect(self):
        self.group_name = "devices_list"

        # Group ga qo'shish
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        print("🔗 New client connected to devices list")

        # Connect bo'lganda barcha devicelarning hozirgi holatini yuborish
        await self.send_all_devices_status()

    async def disconnect(self, close_code):
        # Group dan chiqarish
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("🔌 Client disconnected from devices list")

    async def receive(self, text_data):
        """Mijozdan kelgan xabarlarni qayta ishlash"""
        try:
            data = json.loads(text_data)
            print(f"📨 List consumer received: {data}")

            # Mijoz ma'lum bir so'rov yuborgan bo'lishi mumkin
            if data.get('action') == 'refresh':
                await self.send_all_devices_status()

        except json.JSONDecodeError:
            print(f"❌ Invalid JSON received: {text_data}")

    async def device_status_update(self, event):
        """
        AgentConsumer dan kelgan device status update ini frontendga yuborish
        """
        device_data = event['device_data']
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'device': device_data,
            'timestamp': timezone.now().isoformat()
        }))
        print(f"📤 Sent status update for device: {device_data['bios_uuid']}")

    @database_sync_to_async
    def get_all_devices(self):
        """Barcha devicelarni database dan olish"""
        try:
            devices = Device.objects.all().order_by('-last_seen')
            return [{
                'bios_uuid': str(device.bios_uuid),  # UUID ni string ga aylantirish
                'status': device.status,
                'last_seen': device.last_seen.isoformat() if device.last_seen else None,
                'name': getattr(device, 'name', None),  # Agar name maydoni bo'lsa
                'created_at': device.created_at.isoformat() if hasattr(device,
                                                                       'created_at') and device.created_at else None,
            } for device in devices]
        except Exception as e:
            print(f"❌ Error getting devices: {e}")
            return []

    async def send_all_devices_status(self):
        """
        Connect bo'lganda barcha devicelarning holatini yuborish
        """
        devices = await self.get_all_devices()

        # Barcha devicelarni alohida xabar sifatida yuborish
        for device in devices:
            await self.send(text_data=json.dumps({
                'type': 'initial_status',
                'device': device,
                'timestamp': timezone.now().isoformat()
            }))

        # Jami devicelar sonini ham yuborish
        await self.send(text_data=json.dumps({
            'type': 'devices_count',
            'total_devices': len(devices),
            'online_devices': len([d for d in devices if d['status'] == DeviceStatusChoice.Online]),
            'offline_devices': len([d for d in devices if d['status'] == DeviceStatusChoice.Offline]),
            'timestamp': timezone.now().isoformat()
        }))

        print(f"📤 Sent status for {len(devices)} devices")


class DeviceDetailConsumer(AsyncWebsocketConsumer):
    """
    Bitta device ning batafsil ma'lumotlarini ko'rsatish uchun consumer
    Frontend mijozlar uchun device detail sahifasi
    """

    async def connect(self):
        # URL dan device UUID ni olish
        self.bios_uuid = self.scope['url_route']['kwargs']['bios_uuid']
        self.group_name = f'device_{self.bios_uuid}'

        # Device group ga qo'shish (AgentConsumer bilan bir xil group)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        print(f"🔗 Client connected to device detail: {self.bios_uuid}")

        # Connect bo'lganda device ning hozirgi holatini yuborish
        await self.send_device_status()

    async def disconnect(self, close_code):
        # Group dan chiqarish
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"🔌 Client disconnected from device detail: {self.bios_uuid}")

    async def receive(self, text_data):
        """Mijozdan kelgan xabarlarni qayta ishlash"""
        try:
            data = json.loads(text_data)
            print(f"📨 Detail consumer received: {data}")

            if data.get('action') == 'refresh':
                await self.send_device_status()

        except json.JSONDecodeError:
            print(f"❌ Invalid JSON received: {text_data}")

    async def agent_message(self, event):
        """AgentConsumer dan kelgan xabarlarni mijozga yuborish"""
        await self.send(text_data=json.dumps({
            'type': 'agent_data',
            'data': event['message'],
            'timestamp': timezone.now().isoformat()
        }))

    @database_sync_to_async
    def get_device_detail(self):
        """Device ning batafsil ma'lumotlarini olish"""
        try:
            device = Device.objects.get(bios_uuid=self.bios_uuid)
            return {
                'bios_uuid': str(device.bios_uuid),
                'status': device.status,
                'last_seen': device.last_seen.isoformat() if device.last_seen else None,
                'name': getattr(device, 'name', None),
                'created_at': device.created_at.isoformat() if hasattr(device,
                                                                       'created_at') and device.created_at else None,
                # Qo'shimcha maydonlar qo'shish mumkin
            }
        except Device.DoesNotExist:
            return None

    async def send_device_status(self):
        """Device ning hozirgi holatini yuborish"""
        device_data = await self.get_device_detail()

        if device_data:
            await self.send(text_data=json.dumps({
                'type': 'device_status',
                'device': device_data,
                'timestamp': timezone.now().isoformat()
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Device with UUID {self.bios_uuid} not found',
                'timestamp': timezone.now().isoformat()
            }))