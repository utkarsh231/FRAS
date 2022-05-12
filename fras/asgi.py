"""
ASGI config for fras project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
"""
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,uRLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from dajngo.urls import path
from video.consumers import VideoChat

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fras.settings')

application = ProtocolTypeRouter((
    'websocket':AllowedHostsOriginValidator(
        URLRouter([
            path('ws/',fras.as_asgi())
        ])
    )
))
"""

"""
ASGI config for VideoChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from attds.consumers import VideoChat
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fras.settings')


application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        URLRouter([
            path('ws/',VideoChat.as_asgi())
        ])
    )
})
