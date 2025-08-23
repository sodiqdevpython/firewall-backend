from django.urls import re_path
from hosts import consumers

websocket_urlpatterns = [
    re_path(r'ws/device/(?P<bios_uuid>[0-9a-f-]+)/$', consumers.AgentConsumer.as_asgi()),
    re_path(r"ws/device/fire_wall/(?P<bios_uuid>[^/]+)/$", consumers.DeviceConsumer.as_asgi()),

]
