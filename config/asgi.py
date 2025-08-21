import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # 1) settingsni aniqlash
django.setup()  # 2) django setup qilish

from hosts.routing import websocket_urlpatterns  # 3) endi routingni import qiling

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
