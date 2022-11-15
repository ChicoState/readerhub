from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app1.forms import JoinForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from personalization.models import PersonalInfo
from personalization.models import FavoriteBooks
from books.forms import BooksForm
from books.forms import BookReviewForm
from books.models import BookReview

#import urllib library
from urllib.request import urlopen

# import json
import json


@login_required(login_url='/login/')
def books(request):
    if (request.method == "POST"):
        if ("search_books" in request.POST):
            books_form = BooksForm(request.POST)
            if (books_form.is_valid()):
                book_search = books_form.cleaned_data["book_search"]
                book_search = book_search.replace(" ", "+") #replace spaces with + for query
                json_url = ".json"
                mode = "mode=ebooks" #make sure it has an ebook to filter out garbage submitted books on open library
                text = "has_fulltext=true" #also helps filter out incomplete books
                url = 'https://openlibrary.org/search{}?q={}&{}&{}'.format(json_url, book_search, mode, text )
                response = urlopen(url)
                book_json = json.loads(response.read()) #store json object from url response
                book_cover = []
                book_title = []
                book_id = []
                book_original_id = [] #needed for favoriting the book, need unaltered id
                num_display = 0
                #choosing to display 5 books
                while num_display != 5:
                    #if it reaches how many books were found from query, cannot continue
                    if num_display == book_json["numFound"]:
                        break
                    book_cover.append("http://covers.openlibrary.org/b/id/"+str(book_json["docs"][num_display]["cover_i"])+"-L.jpg") #cover pic
                    book_title.append(book_json["docs"][num_display]["title"]) #title
                    book_temp_id = book_json["docs"][num_display]["key"] #getting id
                    book_original_id.append(book_temp_id) #need this for favorite book
                    book_temp_id = book_temp_id.replace("/", "%") #need to replace backslashes to pass through url or it messes up
                    book_id.append(book_temp_id)
                    num_display = num_display+1
                book_preview = zip(book_title, book_cover, book_id, book_original_id) #combine the lists to be able to display with loop
                context = {
                    "form_data": BooksForm(), #continue displaying form after searching
                    "book_preview": book_preview,
                }
                return render(request,'books/books.html', context)
        elif("favorite" in request.POST): #can also use request.POST.get("favorite")
            cur_user = request.user
            book_id = request.POST.get('favorite')
            book_url = 'https://openlibrary.org{}.json'.format(book_id)
            book_response = urlopen(book_url)
            book_json = json.loads(book_response.read()) #query to store title in FavoriteBooks
            book_title = book_json["title"]
            if 'covers' not in book_json:
                book_cover = "no_book" #doesn't exist
            else:
                book_cover = ("http://covers.openlibrary.org/b/id/"+str(book_json["covers"][0])+"-L.jpg")

            FavoriteBooks(favorite_user = cur_user, favorite_id = book_id, favorite_title = book_title, favorite_cover = book_cover).save()
            context = {
                "form_data": BooksForm(), #continue displaying form
            }
            return render(request,'books/books.html', context)
    else:
        context = {
            "form_data": BooksForm(), #display form
        }
        return render(request, 'books/books.html', context)

def book_view(request, info):
    #replace % signs that were necessary to be  pass book id in url back to backslashes
    info = info.replace("%", "/")
    book_id = info

    #save form data if a book was just reviewed
    #make sure book doesn't already have review from user, important because the form always saves the first form data even if you come from any page
    if not BookReview.objects.filter(user = request.user).exists():
        form = BookReviewForm(request.POST)
        if (form.is_valid()):
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.book_id = book_id
            new_review.star_review = form.cleaned_data['star_review']
            new_review.save()

    #check for review of current book, need to see if review has book id and current user
    text_review = ""
    star_review = 0
    if(BookReview.objects.filter(book_id = book_id).exists() & BookReview.objects.filter(user = request.user).exists()):
        temp_review = BookReview.objects.filter(book_id = book_id) & BookReview.objects.filter(user = request.user)
        #need to use loop to get the one review because filter returns queryset
        for i in temp_review:
            my_review = i
        #store for display in html
        text_review = my_review.text_review
        star_review = my_review.star_review
        my_review_exists = 1
    else:
        my_review_exists = 0



    #query for book information
    book_url = 'https://openlibrary.org{}.json'.format(info)
    book_response = urlopen(book_url)
    book_json = json.loads(book_response.read()) #store json object from url response

    #check if default cover is needed
    if 'covers' not in book_json:
        book_cover = "no_book"
    else:
        book_cover = "http://covers.openlibrary.org/b/id/"+str(book_json["covers"][0])+"-L.jpg"

    book_title = book_json["title"]
    if 'description' not in book_json:
        book_description = "There is no description available."
    else:
        book_description = book_json["description"]

    book_subjects = []
    i = 0
    for subject in book_json["subjects"]: #getting the first 4 subjects listed on page
        if i == 4:
            break
        book_subjects.append(subject)
        i = i+1

    #getting author json object to get author information
    author_id = book_json["authors"][0]["author"]['key']
    author_url = 'https://openlibrary.org{}.json'.format(author_id)
    author_response = urlopen(author_url)
    author_json = json.loads(author_response.read()) #store json object from url response
    author_name = author_json["personal_name"]

    if 'photos' not in author_json:
        author_image = "no_photo"
    else:
        author_image = "https://covers.openlibrary.org/a/id/" + str(author_json["photos"][0]) + "-L.jpg"

    context = {
        "form_data": BooksForm(),
        "book_cover": book_cover,
        "book_title": book_title,
        "book_description": book_description,
        "book_subjects": book_subjects,
        "book_id": book_id,
        "author_name": author_name,
        "author_image": author_image,
        "text_review": text_review,
        "star_review": star_review,
        "my_review_exists": my_review_exists,
    }
    return render(request, 'books/book_view.html', context)

def book_review(request):
    if("review" in request.POST):  #review button was clicked
        #passed in book id with review post request
        book_id = request.POST.get("review")

        #query for cover and title display
        book_url = 'https://openlibrary.org{}.json'.format(book_id)
        book_response = urlopen(book_url)
        book_json = json.loads(book_response.read())
        if 'covers' not in book_json:
            book_cover = "no_book"
        else:
            book_cover = "http://covers.openlibrary.org/b/id/"+str(book_json["covers"][0])+"-L.jpg"
        book_title = book_json["title"]

        #get book_id in correct form to pass through url to view book page
        book_id = book_id.replace("/", "%")
        context = {
            "form_data": BookReviewForm(),
            #cover and title for display on review page
            "book_cover": book_cover,
            "book_title": book_title,
            "book_id": book_id,
        }
        return render(request, 'books/book_review.html', context)
