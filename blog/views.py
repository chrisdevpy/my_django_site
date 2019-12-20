from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_for_frontend = {'posts': posts}
    # to render the template and goes to the stated html file
    return render(request, 'blog/post_list.html',  stuff_for_frontend)

# pk means primary key
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    stuff_for_frontend = {'post': post}
    return render(request, 'blog/post_detail.html', stuff_for_frontend)

def post_new(request):
    # Everything within the if statement (excluding the else statement) is for
    # when anyone does a "submit request", post request.
    if request.method == 'POST':
        # (for line 23) To get access to the text and title from Post (models).
        form = PostForm(request.POST)
        # is_valid() is to get clean input from the user.
        if form.is_valid():
            # commit means to create/save an object in the data base.
            post = form.save(commit=False)
            # (for line 28) The author is anyone who is currently logged in and put that in the data base.
            post.author = request.user
            post.save()
            # (for line 33) Using redirect to only post once and then redirect to a different page.
            return redirect('post_detail', pk=post.pk)
    else:  # Within this else statement is for a GET request
        form = PostForm()
        stuff_for_frontend = {'form': form}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # updating an existing form
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, 'blog/post_draft_list.html', stuff_for_frontend)

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)