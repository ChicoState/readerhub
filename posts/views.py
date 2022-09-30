from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from posts.forms import PostForm

# Create your views here.

@login_required(login_url='/login/')
def posts(request):
    if (request.method == "GET" and "delete" in request.GET):
        id = request.GET["delete"]
        Post.objects.filter(id=id).delete()
        return redirect("/posts/")
    else:
        posts = Post.objects.filter(user=request.user)
        context = {
            "posts": posts,
        }
    return render(request, 'posts/posts.html', context)

@login_required(login_url='/login/')
def add_post(request):
    if (request.method == "POST"):
        if ("add" in request.POST):
            form = PostForm(request.POST)
            if (form.is_valid()):
                newPost = form.save(commit=False)
                newPost.user = request.user
                newPost.save()
                return redirect("/posts/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, "posts/add_post.html", context)
        else:
            return redirect("/posts/")
    else:
        context = {
            "form_data": PostForm()
        }
        return render(request, "posts/add_post.html", context)

@login_required(login_url="/login/")
def edit_post(request, id):
    if (request.method == "GET"):
        item = Post.objects.get(id=id)
        form = PostForm(instance=item)
        context = {
            "form_data": form
        }
        return render(request, "posts/edit.html", context)
    elif (request.method == "POST"):
        if ("edit" in request.POST):
            form = PostForm(request.POST)
            if (form.is_valid()):
                post = form.save(commit=False)
                post.user = request.user
                post.id = id
                post.save()
                return redirect("/posts/")
            else:
                context = {
                    "form_data": form
                }
                return render(request, "posts/add_post.html", context)
        else:
            return redirect("/posts/")
