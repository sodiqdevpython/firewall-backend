from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/device/(?P<bios_uuid>[0-9a-f-]+)/$', consumers.AgentConsumer.as_asgi()),
    re_path(r'ws/devices/$', consumers.DevicesListConsumer.as_asgi()),
    re_path(r'ws/device-detail/(?P<bios_uuid>[0-9a-f-]+)/$', consumers.DeviceDetailConsumer.as_asgi()),
]