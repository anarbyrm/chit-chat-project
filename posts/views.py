from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Post, Comment
from .forms import ContactForm, PostCreateForm, CommentCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def welcome(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'welcome.html')


def feed(request):
    posts_ = Post.objects.all()
    comments = Comment.objects.all()[:5]
    context = {'posts_':posts_, 'comments':comments}
    return render(request, 'feed.html', context)


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Your message has been delivered to the admin')
            return redirect('feed')
            
    context={'form':form}
    return render(request, 'contact.html', context)


#CRUD
@login_required()
def post_create(request):
    form = PostCreateForm()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostCreateForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                form.save()
                messages.success(request, 'New post added to the feed...')
                return redirect('feed')

    context = {'form': form}
    return render(request, 'post_create_update.html', context)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comment_set.all()
    form = CommentCreationForm()

    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            user_comment = form.save(commit=False)
            user_comment.user = request.user
            user_comment.post = post
            form.save()
            return redirect('post_detail', pk=pk)
    context = {'post': post, 'comments': comments, 'form':form}
    return render(request, 'post_detail.html', context)


@login_required
def post_update(request, pk):
    obj = get_object_or_404(Post, id=pk)
    form = PostCreateForm(instance=obj)
    if obj.author == request.user:
        if request.method == 'POST':
            form = PostCreateForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect("post_detail", pk=pk)
    else:
        return HttpResponse("<h1>Sorry, you don't have permission from the author to update the post! (X_X) </h1>")
    
    context = {'form': form, 'obj': obj}
    return render(request, 'post_create_update.html', context)

@login_required()
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST" and not None:
        post.delete()
        messages.info(request, 'Post has been deleted!')
        return redirect('feed')
        
    context = {'post':post}
    return render(request, "post_delete.html", context)