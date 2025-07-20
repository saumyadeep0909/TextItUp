"""
ASGI config for messenger_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import messenger.routing
from django.core.asgi import get_asgi_application
import messenger.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger_project.settings')

application = ProtocolTypeRouter({
    "http" : get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messenger.routing.websocket_urlpatterns
        )
    ),
})
