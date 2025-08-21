import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import applications.routing as applications_routing
import hosts.routing as host_routing
import logs.routing as logs_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            applications_routing.websocket_urlpatterns
            + logs_routing.websocket_urlpatterns + host_routing.websocket_urlpatterns
        )
    ),
})