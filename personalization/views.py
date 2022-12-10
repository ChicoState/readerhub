# pylint: disable=E5142, C0209
""" profile, edit profile, add friend, see friends """
#imports needed for favorite books on profile page (urlopen and json)
from urllib.request import urlopen
import json
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from personalization.models import PersonalInfo, Follows, FavoriteBooks
from personalization.forms import PersonalInfoForm, FollowForm
from posts.models import Post

@login_required(login_url='/login/')
def personalization(request, name):
    """ profile page """
    user = User.objects.get(username=name)
    req_username = user.username
    if request.method == 'POST':
        user = request.user
        follow = User.objects.get(username = name)
        Follows.objects.get_or_create(user_id=user.id, following_user_id=follow.id)
        return redirect('/personalization/%s' % user.username )

    profile = PersonalInfo.objects.get(user=user) #the user personal info
    posts = Post.objects.filter(user=user) #posts the user has made
    following = user.following.all()
    followers = user.followers.all()
    already_follows = False
    try:
        Follows.objects.get(user_id=request.user.id, following_user_id=user.id)
        already_follows = True
    except:
        already_follows = False
    if posts:
        for post in posts:
            post.book_object.favorite_id = post.book_object.favorite_id.replace("/", "%")
    if not FavoriteBooks.objects.filter(user=user):
        context = {
            "profile": profile,
            "posts": posts,
            "following": following,
            "followers": followers,
            "req_user": req_username,
            "al_fol": already_follows,
        }
        return render(request, 'personalization/personalization.html', context)

    favorite_books = FavoriteBooks.objects.filter(user	= user)
    favorite_covers = []
    favorite_titles = []
    for book in favorite_books:
        book_url = 'https://openlibrary.org{}.json'.format(book.favorite_id)
        book_response = urlopen(book_url)
        book_json = json.loads(book_response.read()) #store json object from url response
        if 'covers' not in book_json:
            favorite_covers.append("no_book") #doesn't exist
        else:
            favorite_covers.append("http://covers.openlibrary.org/b/id/"+str(book_json["covers"][0])+"-L.jpg")
        favorite_titles.append(book_json["title"])

    context = {
        "profile": profile,
        "posts": posts,
        "favorite_books": favorite_books,
        "following": following,
        "followers": followers,
        "req_user": req_username,
        "al_fol": already_follows,
    }
    return render(request, 'personalization/personalization.html', context)

def edit_profile(request, id):
    """ edit profile page """
    if request.method == "GET":
        # Load personal info form with current model data.
        personalInfo = PersonalInfo.objects.get(id=id)
        form = PersonalInfoForm(instance=personalInfo)
        user = personalInfo.user
        context = {
            "form_data": form,
            "user": user, #to display username in html
        }
        return render(request, 'personalization/edit_profile.html', context)
    elif request.method == "POST":
        # Process form submission
        if "edit" in request.POST:
            form = PersonalInfoForm(request.POST, request.FILES)
            if form.is_valid():
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
                return redirect('personalization', name=request.user.username)
            context = {
                "form_data": form
            }
            return render(request, 'personalization/edit_profile.html', context)
        #Cancel
        return redirect('personalization', name=request.user.username)
    #### Should return something here ####

def add_friend(request):
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            user = request.user
            following = user.following.all()
            followers = user.followers.all()
            try:
                follow = User.objects.get(username = form.cleaned_data['userName'])
            except User.DoesNotExist:
                context = {
                    "form": form,
                    "dne": form.cleaned_data["userName"],
                    'following': following,
                    'followers': followers,
                }
                return render(request, "personalization/add_friend.html", context)
            Follows.objects.get_or_create(user_id=user.id, following_user_id=follow.id)
            return redirect("/addFriends/")
    user = request.user
    following = user.following.all()
    followers = user.followers.all()
    context = {
        'form': FollowForm() ,
        'following': following,
        'followers': followers,
    }
    return render(request, 'personalization/add_friend.html', context)
