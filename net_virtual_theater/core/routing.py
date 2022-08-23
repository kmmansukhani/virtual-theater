from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/waitingroom/<str:party_id>/', consumers.WaitingRoomConsumer.as_asgi()),
] 