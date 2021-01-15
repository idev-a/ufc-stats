# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from contest.routing import websockets
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": websockets,
})

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack( websockets ),
# })