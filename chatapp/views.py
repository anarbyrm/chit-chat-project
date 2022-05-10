from django.shortcuts import render, redirect
from .models import Chat, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

#chat thread list
@login_required()
def inbox(request):
    chats = Chat.objects.filter(Q(chat_sender=request.user) | Q(chat_receiver=request.user))

    context = {'chats': chats}
    return render(request, 'inbox.html', context)


#single chat view
@login_required()
def chat_detail(request, pk):
    form = None
    chat = Chat.objects.get(id=pk)
    msgs = chat.message_set.all()
    
    if chat.chat_receiver == request.user:
        reply = chat.chat_sender
    elif chat.chat_sender == request.user:
        reply = chat.chat_receiver
    
    if request.method == "POST":
        try:
            form = Message(
                chat=chat,
                message_sender=request.user,
                message_receiver=reply,
                body=request.POST.get('body')
            )
        except DoesNotExist:
            messages.info(request, 'Sorry, there is no such user!')
            return redirect('inbox')

        form.save()
        return redirect('chat_detail', pk=pk)
        
    context = {'chat': chat, 'msgs': msgs, 'form':form}
    return render(request, 'chat_detail.html', context)


#creating chat
@login_required()
def chat_create(request):
    chat = Chat()
    if request.method == "POST":
        user = request.POST.get('user')
        user = User.objects.get(username=user)

        chat = Chat(
            chat_sender=request.user,
            chat_receiver=user
        )

        if Chat.objects.filter(chat_sender=user, chat_receiver=request.user).exists():
            chat = Chat.objects.filter(chat_sender=user, chat_receiver=request.user).first()
            return redirect('chat_detail', pk=chat.id)
        elif Chat.objects.filter(chat_sender=request.user, chat_receiver=user).exists():
            chat = Chat.objects.filter(chat_sender=request.user, chat_receiver=user).first()
            return redirect('chat_detail', pk=chat.id)
        else:
            chat.save()
            return redirect('inbox')

    context = {'chat': chat}
    return render(request, 'chat_create.html', context)



