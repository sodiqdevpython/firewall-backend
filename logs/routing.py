from django.urls import re_path
from .consumers import AgentLogConsumer

websocket_urlpatterns = [
    re_path(r"ws/agentlogs/$", AgentLogConsumer.as_asgi()),
]
