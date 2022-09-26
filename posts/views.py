from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from posts.forms import PostForm

# Create your views here.

@login_required(login_url='/login/')
def posts(request):

