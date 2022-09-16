from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from personalization.models import PersonalPage
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
import requests



@login_required(login_url='/login/')
#create personal page
