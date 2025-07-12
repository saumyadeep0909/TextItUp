from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm 
from .forms import MessageForm
from .models import Message
from django.contrib.auth.decorators import login_required
from .forms import LoginForm 
from django.contrib.auth.models import User
from django.db.models import Q


def home(request):
    if request.user.is_authenticated:
        return redirect('inbox')
    else:
        return redirect('login')
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'messenger/signup.html',{'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #Authenticate returns a User object
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # nly works if `user` is a real User, not coroutine
                return redirect('inbox')
            else:
                print("Invalid Credentials")
    else:
        form = LoginForm()
    return render(request, 'messenger/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def inbox(request):
    current_user = request.user

    
    conversations = Message.objects.filter(
        Q(sender=current_user) | Q(recipient=current_user)
    ).order_by('-timestamp')

    if conversations.exists():
        # Get the most recent conversation partner
        latest_msg = conversations.first()
        chat_partner = latest_msg.recipient if latest_msg.sender == current_user else latest_msg.sender
        return redirect('chat', user_id=chat_partner.id)
    
    # If no messages, show list of users to start new chat
    users = User.objects.exclude(id=current_user.id)
    return render(request, 'messenger/inbox.html', {
        'users': users,
        'has_messages': False,
    })


@login_required
def send_message(request, user_id):
    recipient = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            return redirect('chat', user_id=recipient.id)
    else:
        form = MessageForm()
    return render(request, 'messenger/send.html', {
        'form': form,
        'recipient': recipient
    })

@login_required
def chat_view(request, user_id):
    all_users = User.objects.exclude(id=request.user.id)
    recipient = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            return redirect('chat', user_id=recipient.id)
    else:
        form = MessageForm()

    
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-timestamp')

    chat_users = list(set(
        [msg.sender for msg in conversations if msg.sender != request.user] +
        [msg.recipient for msg in conversations if msg.recipient != request.user]
    ))

    room_name = '_'.join(sorted([request.user.username, recipient.username]))

    return render(request, 'messenger/chat.html', {
        'form': form,
        'recipient': recipient,
        'messages': messages,
        'chat_users': chat_users,
        'all_users':all_users,
        'room_name': room_name,
    })