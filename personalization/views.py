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
import requests



@login_required(login_url='/login/')
def profile(request):
	if (request.method == "GET" and "delete" in request.GET):
            id = request.GET["delete"]
            RecipeEntry.objects.filter(id=id).delete()
            return redirect("personalization/profile.html")
	else:
            table_data = PersonalInfo.objects.filter(user=request.user) #all recipes the user has
            print(PersonalInfo.objects.filter(favorite_books=request.user))
            context = {
                "table_data": table_data,
            }
            return render(request, 'personalization/profile.html', context)


@login_required(login_url='/login/')
def add_profile(request):
    if (request.method == "POST"):
        if ("add_profile" in request.POST):
            add_form = PersonalInfoForm(request.POST, request.FILES)
            if (add_form.is_valid()):  #entering recipe attributes @@@@@@
                favorite_books = add_form.cleaned_data["favorite_books"]
                about_user = add_form.cleaned_data["about_user"]
                personal_image = add_form.cleaned_data["personal_image"]
                user = User.objects.get(id=request.user.id)
                print("TEST")
                PersonalInfo(user=user, favorite_books = favorite_books, about_user = about_user, personal_image = personal_image).save()
                return redirect("/personalization/profile")
            else:
                context = {
                    "form_data": add_form,
                }
                return render(request, 'personalization/add_profile.html', context)
        else:
			# Cancel
            return redirect("personalization/profile/")
    else:
        context = {
            "form_data": PersonalInfoForm(),
        }
        return render(request, 'personalization/add_profile.html', context)
