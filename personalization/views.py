from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from personalization.models import PersonalInfo
from personalization.forms import PersonalInfoForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from readerhub import settings
import requests
import os



@login_required(login_url='/login/')
def personalization(request):
	try: #display profile created with form
		profile = PersonalInfo.objects.get(user=request.user) #the user personal info
		context = {
			"profile": profile,
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
	#	print(personalInfo.personal_image)
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
