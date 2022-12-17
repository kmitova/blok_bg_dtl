from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from dmmessages.models import ChatMessage

UserModel = get_user_model()


def get_unread_messages(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = ChatMessage.objects.filter(user=request.user, is_read=False).count()

    context = {
        'unread_count': unread_count,
    }

    return context


@login_required
def inbox_page(request):
    user = request.user
    messages = ChatMessage.get_messages(user=user)
    active_direct = None
    directs = None
    context = {}

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = ChatMessage.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            print(message['unread'])

        context = {
            'directs': directs,
            'messages': messages,
            'active_direct': active_direct
        }

    return render(request, 'messages/inbox.html', context)


@login_required
def send_message(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    if request.method == 'POST':
        to_user = UserModel.objects.get(username=to_user_username)
        ChatMessage.send_message(from_user, to_user, body)
        return redirect('chat', username=to_user_username)
    else:
        return HttpResponseBadRequest()


@login_required
def chat_page(request, username):
    user = request.user
    recipient = UserModel.objects.filter(username=username).get()
    messages = ChatMessage.objects.filter(user=user, recipient=recipient).order_by('date')
    active_direct = username
    directs = ChatMessage.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message.user.username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'recipient': recipient
    }

    return render(request, 'messages/chat.html', context)
