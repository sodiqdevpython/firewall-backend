import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import urlparse, parse_qs

class ConnectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("connections", self.channel_name)
        host_group = self._get_host_group()
        if host_group:
            await self.channel_layer.group_add(host_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("connections", self.channel_name)
        host_group = self._get_host_group()
        if host_group:
            await self.channel_layer.group_discard(host_group, self.channel_name)

    def _get_host_group(self):
        try:
            qs = parse_qs(urlparse(self.scope["query_string"].decode()).query)
        except Exception:
            qs = {}
        host_id = (qs.get("host_id") or [None])[0]
        return f"host_{host_id}" if host_id else None

    async def connection_created(self, event):
        await self.send(text_data=json.dumps(event["data"]))
