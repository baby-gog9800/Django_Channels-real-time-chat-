from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404,redirect

@login_required
def ChatView(request):
    form_create = ChatRoomCreateForm()
    form_search = ChatRoomSearchForm()
    if request.method == "GET" :
        print(request.GET)
        if 'create_chatroom' in request.GET:
            form_create = ChatRoomCreateForm(request.GET)
            if form_create.is_valid():
                cd = form_create.cleaned_data
                chatroom = ChatRoom()
                chatroom.chatroom_name = cd['chatroom_name']
                chatroom.save()
                chatroom.users.add(request.user)
                chatroom.save()
                chatroom = ChatRoom.objects.get(chatroom_name=cd['chatroom_name'])
                return redirect('chatroom',chatroom_name=cd['chatroom_name'])
        else:
            form_search = ChatRoomSearchForm(request.GET)
            if form_search.is_valid():
                chatroom = form_search.cleaned_data['chatroom_name']
                return redirect("chatroom",chatroom_name=chatroom)

    return render(request,'chat/chat.html',{'form_search':form_search,'form_create':form_create})

@login_required
def ChatRoomView(request,chatroom_name):
    try:
        chatroom = ChatRoom.objects.get(chatroom_name=chatroom_name)
        return render(request,'chat/chat_room.html',{'chat_room_name':chatroom_name})
    except ChatRoom.DoesNotExist:
        return redirect('chat')
