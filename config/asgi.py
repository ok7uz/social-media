import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import apps.chat.routing
import apps.notification.routing
from apps.chat.middleware import JwtAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        JwtAuthMiddleware(
            URLRouter(apps.chat.routing.websocket_urlpatterns + apps.notification.routing.websocket_urlpatterns)
        )
    )
})
