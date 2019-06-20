from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from chat import consumer

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(
        URLRouter([
            url(r'^ws/chat/(?P<chat_room_name>[^/]+)/$', consumer.ChatConsumer),
            url(r'^ws/chat/$', consumer.SearchConsumer),
        ])
    )
})
