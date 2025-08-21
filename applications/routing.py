from django.urls import re_path
from .consumers import ApplicationConsumer
from .consumers_connections import ConnectionConsumer

websocket_urlpatterns = [
    re_path(r"ws/applications/$", ApplicationConsumer.as_asgi()),
    re_path(r"ws/connections/$", ConnectionConsumer.as_asgi()),
]
