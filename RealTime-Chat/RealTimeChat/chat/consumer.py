from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from django.shortcuts import redirect
from channels.db import database_sync_to_async
from .models import *
import json

class ChatConsumer(AsyncConsumer):
    @database_sync_to_async
    def get_ChatRoom(self,chat_room_name):
        try:
            chatroom = ChatRoom.objects.get(chatroom_name=chat_room_name)
            return chatroom

        except ChatRoom.DoesNotExits:
            return None

    @database_sync_to_async
    def get_Messages(self,chatroom):
        messages = []
        for i in chatroom.message.all():
            messages.append([i.message,i.sender.username])
        return messages

    @database_sync_to_async
    def save_Message(self,user,chatroom,message):
        chat_message = ChatMessage()
        chat_message.sender = user
        chat_message.message = message
        chat_message.chatroom = chatroom
        chat_message.save()
        return chat_message

    async def websocket_connect(self,event):
        self.chat_room_name = self.scope['url_route']['kwargs']['chat_room_name']
        await self.send({
            'type':'websocket.accept',
        })

        await self.channel_layer.group_add(
            self.chat_room_name,
            self.channel_name
        )

        chatroom = await self.get_ChatRoom(self.chat_room_name)
        if chatroom:
            messages = await self.get_Messages(chatroom)
        else:
            redirect('chat')

        data = {
            'messages' : messages,
                }
        await self.send({
            'type':'websocket.send',
            'text': json.dumps(data),
        })
        data_={
            'message_active':"is active in chatroom.",
            'user': self.scope["user"].username
        }
        await self.channel_layer.group_send(
            self.chat_room_name,
            {
                'type' : 'incoming_msg_ws',
                'message': json.dumps(data_),
            }

        )


    async def websocket_disconnect(self,event):
        data_={
            'message_active':"left the chatroom.",
            'user': self.scope["user"].username
        }
        await self.channel_layer.group_send(
            self.chat_room_name,
            {
                'type' : 'incoming_msg_ws',
                'message': json.dumps(data_),
            }
        )
        raise StopConsumer()

    async def websocket_receive(self,event):
        user = self.scope["user"]
        chatroom = await self.get_ChatRoom(self.chat_room_name)
        incoming_msg_ws = json.loads(event['text'])
        if chatroom:
            chat_message=await self.save_Message(user,chatroom,incoming_msg_ws['message'])
            data_ = {
                'message':chat_message.message,
                'user':chat_message.sender.username
            }
            return await self.channel_layer.group_send(
                    self.chat_room_name,
                    {
                        'type' : 'incoming_msg_ws',
                        'message': json.dumps(data_),
                    })
        else:
            return redirect('chat')

    async def incoming_msg_ws(self,event):
        send_data = {
            'type'   : "websocket.send",
            'text': event["message"],
        }
        return await super().send(send_data)




class SearchConsumer(AsyncConsumer):
    @database_sync_to_async
    def searchQuery(self,query):
        rooms_ = ChatRoom.objects.filter(chatroom_name__icontains=query)
        rooms = []
        for i in rooms_:
            rooms.append(i.chatroom_name)
        return rooms

    async def websocket_connect(self,event):
        await self.send({
            'type' : 'websocket.accept',
        })

    async def websocket_receive(self,event):
        query = event["text"]
        rooms_ =await self.searchQuery(query)
        data = {
            'rooms':rooms_
        }
        return await super().send({
            'type':'websocket.send',
            'text':json.dumps(data),
        })


    async def websocket_disconnect(self,event):
        await self.send({
            'type' : 'websocket.disconnect'
        })
        raise StopConsumer()
