# restaurant/routing.py
from django.urls import path,re_path
from .consumers import MessageConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/', MessageConsumer.as_asgi()),
]
