from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post


# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            u = request.POST.get('u')
            p = request.POST.get('p')
            user = authenticate(request, username=u, password=p)
            if user is not None:
                login(request, user)
                return redirect('feed')
    else:
        messages.info(request, f"{request.user.username}, you already logged in!")
        return redirect('feed')

    return render(request, 'login.html')


def register_view(request):
    form = UserCreationForm()
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created! You can login now.')
                return redirect('login')
    else:
        messages.info(request, f'{request.user.username}, you already have an account!')
        return redirect('feed')

    context = {'form': form}
    return render(request, 'register.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            logout(request)
            return redirect('welcome')
    else:
        return redirect('welcome')
    return render(request, 'logout.html')


@login_required()
def profile_view(request, username):
    posts = Post.objects.all()
    username = User.objects.filter(username=username).first()
    if username:
        posts = Post.objects.filter(author=username)
    else:
        messages.info(request, 'No such user was found!')
        return redirect('feed')

    context = {'posts': posts, 'username':username}
    return render(request, 'profile.html', context)


