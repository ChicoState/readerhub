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
    if (request.method == "GET"):
        #info is book id passed through url
        info = info.replace("%", "/") #replace @ signs that were necessary to be passed in url back to backslashes
        book_id = info
        book_url = 'https://openlibrary.org{}.json'.format(info)
        book_response = urlopen(book_url)
        book_json = json.loads(book_response.read()) #store json object from url response


        if 'covers' not in book_json:
            book_cover = "no_book" #doesn't exist
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
        }
        return render(request, 'books/book_view.html', context)
def book_review(request):
    if("review" in request.POST):  #review button was clicked
        context = {
            "form_data": BookReviewForm(), #display form
        }
        return render(request, 'books/book_review.html', context)
    elif("submit_review" in request.POST):
        form = BookReviewForm(request.POST)
        if (form.is_valid()):
            print(form.cleaned_data['star_review'])
        #    new_review = form.save(commit=False)
        #    new_review.user = request.user
        #    new_review.book_id.save()
        return render(request, 'books/book_review.html')
