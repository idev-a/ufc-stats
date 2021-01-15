from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import LiveScoreConsumer

websockets = URLRouter([
    re_path(
        r"^ws/ufc-event/$", LiveScoreConsumer.as_asgi(),
        name="live-score",
    ),
])