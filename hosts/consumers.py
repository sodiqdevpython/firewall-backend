import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from hosts.choices import DeviceStatusChoice
from hosts.models import Device


class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['bios_uuid']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        device_updated = await self.set_online()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        device_updated = await self.set_offline()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'agent_message',
                    'message': data
                }
            )
        except json.JSONDecodeError:
            print(f"Invalid JSON")

    async def agent_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'agent_data',
            'data': event['message']
        }))

    @database_sync_to_async
    def set_online(self):
        device = Device.objects.get(bios_uuid=self.room_name)
        print(device, 11111111111111111)
        device.status = DeviceStatusChoice.Online
        device.save(update_fields=["status"])

    @database_sync_to_async
    def set_offline(self):
        device = Device.objects.get(bios_uuid=self.room_name)
        device.status = DeviceStatusChoice.Offline
        device.last_seen = timezone.now()
        device.save(update_fields=['status', 'last_seen'])

    @database_sync_to_async
    def get_device_status(self):
        device = Device.objects.get(bios_uuid=self.room_name)
        return {
            "bios_uuid": str(device.bios_uuid),
            "status": device.status,
            "last_seen": device.last_seen.isoformat() if device.last_seen else None,
            "name": getattr(device, "name", None)
        }


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "all_devices"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def firewall_rule(self, event):
        await self.send(text_data=json.dumps({
            "type": "firewall_rule",
            "event": event.get("event", "unknown"),
            "data": event["rule"]
        }))
