# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import restaurant.routing  # Import your routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            restaurant.routing.websocket_urlpatterns
        )
    ),
})
