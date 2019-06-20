from django.urls import path
from .views import *
urlpatterns=[
    path('',ChatView,name='chat'),
    path('chatroom/<str:chatroom_name>',ChatRoomView,name='chatroom')
]
