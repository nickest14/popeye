from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from popeye.auth import WebSocketAuthMiddlewareStack
from popeye.consumers import CustomConsumer


application = ProtocolTypeRouter({
    "websocket": WebSocketAuthMiddlewareStack(
        URLRouter([
            url(r'ws$', CustomConsumer)
        ]),
    ),
})
