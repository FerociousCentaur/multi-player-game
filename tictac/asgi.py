"""
ASGI config for tictac project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os

import django
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.layers import get_channel_layer
from home.consumers import GameRoom
from django.core.asgi import get_asgi_application
from django.urls import path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tictac.settings')
django.setup()
#application = get_asgi_application()
channel_layer = get_channel_layer()

ws_pattern = [
        path('ws/game/<room_code>', GameRoom.as_asgi())
]


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket':URLRouter(
            ws_pattern
        )
    })
