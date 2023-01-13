import os

from chat.middleware import WebSocketJwtAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WebSocketJwtAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)
