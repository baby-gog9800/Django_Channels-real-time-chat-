from django.db import models as mdb
from django.contrib.auth.models import User

class ChatRoom(mdb.Model):
    time_created = mdb.DateTimeField(auto_now=True)
    chatroom_name = mdb.CharField(unique=True,max_length=200)
    users = mdb.ManyToManyField(User)
    time_active = mdb.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chatroom_name

class ChatMessage(mdb.Model):
    sender = mdb.ForeignKey(User, on_delete=mdb.CASCADE)
    message = mdb.TextField(blank = True,null = True)
    time = mdb.DateTimeField(auto_now=True)
    chatroom = mdb.ForeignKey(ChatRoom, related_name='message',on_delete=mdb.CASCADE)

    def __str__(self):
        return str(self.message)
