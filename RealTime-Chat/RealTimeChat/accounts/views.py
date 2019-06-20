from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate as authen, login, logout
from .models import *
from .forms import *
from django.contrib.auth import authenticate

def Logout(request):
    logout(request)
    return redirect('login')

def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authen(username=cd['username'], password=cd['password'])
            # print(user)
            if user:
                login(request,user)
                return redirect('chat')
    else:
        form = LoginForm()
        return render(request,'accounts/login.html',{'form':form,})
    return render(request,'accounts/login.html',{'form':form,'error':"User DoesNot Exists"})

def SignUp(request):
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                print(cd)
                user = User.objects.create_user(cd['username'],cd['email'],cd['password'])
                user.save()
                user = authen(username=cd['username'], password=cd['password'])
                login(request,user)
                return redirect('chat')
                # return render(request,'chat/chat.html',{'user':user})
        else:
            form = SignUpForm()
        return render(request,'accounts/signup.html',{'form':form})
