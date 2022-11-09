from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from personalization.models import PersonalInfo, Follows, FavoriteBooks
from personalization.forms import PersonalInfoForm, FollowForm
from posts.models import Post
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from readerhub import settings
import requests
import os
#imports needed for favorite books on profile page
from urllib.request import urlopen
import json



@login_required(login_url='/login/')
def personalization(request):
	try: #display profile created with form
		profile = PersonalInfo.objects.get(user=request.user) #the user personal info
		posts = Post.objects.filter(user=request.user) #posts the user has made
		following = request.user.following.all()
		followers = request.user.followers.all()
		if not FavoriteBooks.objects.filter(favorite_user=request.user):
			context = {
				"profile": profile,
				"posts": posts,
				"following": following,
				"followers": followers,
			}
			return render(request, 'personalization/personalization.html', context)
		else:
			favorite_books = FavoriteBooks.objects.filter(favorite_user	=request.user)
			max_books = 0 #counting number of books being chosen to display
			favorite_covers = []
			favorite_titles = []
			for book in favorite_books:
				if max_books == 4:
					break
				book_url = 'https://openlibrary.org{}.json'.format(book.favorite_id)
				book_response = urlopen(book_url)
				book_json = json.loads(book_response.read()) #store json object from url response
				if 'covers' not in book_json:
					favorite_covers.append("no_book") #doesn't exist
				else:
					favorite_covers.append("http://covers.openlibrary.org/b/id/"+str(book_json["covers"][0])+"-L.jpg")
				favorite_titles.append(book_json["title"])
				max_books = max_books+ 1

			favorite_preview = zip(favorite_titles, favorite_covers)#combine for displaying in for loop in html
			context = {
				"profile": profile,
				"posts": posts,
				"favorite_preview": favorite_preview,
				"following": following,
				"followers": followers,
			}
			return render(request, 'personalization/personalization.html', context)
	except PersonalInfo.DoesNotExist: #making default profile if it doesnt exist
		PersonalInfo(user = request.user).save()
		profile = PersonalInfo.objects.get(user=request.user)
		context = {
			"profile": profile,
		}
		return render(request, 'personalization/personalization.html', context)



def edit_profile(request, id):
	if (request.method == "GET"):
		# Load personal info form with current model data.
		personalInfo = PersonalInfo.objects.get(id=id)
		form = PersonalInfoForm(instance=personalInfo)
		user = personalInfo.user
		context = {
		"form_data": form,
		"user": user, #to display username in html
		}
		return render(request, 'personalization/edit_profile.html', context)
	elif (request.method == "POST"):
		# Process form submission
		if ("edit" in request.POST):
			form = PersonalInfoForm(request.POST, request.FILES)
			if (form.is_valid()):
				personalInfoTemp = PersonalInfo.objects.get(id=id) #getting object for image deletion
				personalInfo = form.save(commit=False)
				personalInfo.user = request.user
				personalInfo.id = id
				if not personalInfo.personal_image: #no new image chosen
					if personalInfoTemp.personal_image: #make sure this is not first time putting image
						personalInfo.personal_image = personalInfoTemp.personal_image #save image old if new one is not chosen
				else: #new image is chosen
					if personalInfoTemp.personal_image: #an old image exists
						os.remove(personalInfoTemp.personal_image.path) #removes old image file from images when image is changed
				personalInfo.save()
				return redirect("/personalization/")
			else:
				context = {
                    "form_data": form
				}
				return render(request, 'personalization/edit_profile.html', context)
		else:
			#Cancel
			return redirect("/personalization/")

def add_friend(request):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            user = request.user
            follow = User.objects.get(username = form.cleaned_data['userName'])
            Follows.objects.create(user_id=user.id, following_user_id=follow.id)
            return redirect('/')
    context = { 'form': FollowForm() }
    return render(request, 'personalization/add_friend.html', context)

def see_friends(request):
    user = request.user
    following = user.following.all()
    followers = user.followers.all()
    context = {
        'following': following,
        'followers': followers,
    }
    return render(request, 'personalization/follows.html', context)
