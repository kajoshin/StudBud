from functools import reduce

from django.db.transaction import commit
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.
# rooms = [
#     {'id': 1, 'name': "Let's learn Python"},
#     {'id': 2, 'name': "Backend Developers"},
#     {'id': 3, 'name': "Frontend Developers"}
# ]

def login_page(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"User or Password does not exist ")


    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page='register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    return render (request, 'base/login_register.html',{'form':form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages}
    return render(request, "base/home.html", context)


def room(request, pk):
    room =Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user,'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html',context)


@login_required(login_url="/login")
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "base/room_form.html", context)

@login_required(login_url="/login")
def update_room(request, pk):
    r = Room.objects.get(id=pk)
    form = RoomForm(instance=r)

    if request.user != r.host:
        return HttpResponse("You are not allowed here - not your room.")
    if request.method == 'POST':
        form = RoomForm(request.post, instance=r)
        if form.is_valid():
            form.save()
            redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="/login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != r.host:
        return HttpResponse("You are not allowed here - not your room.")

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url="/login")
def delete_message(request, pk):
   # room = Room.objects.get(id=rPk)
    message = Message.objects.get(id=pk)
    if request.user !=  message.user:
        return HttpResponse("You are not allowed here ")

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})