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
from books.forms import BooksForm

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
                num_display = 0
                #choosing to display 5 books
                while num_display != 5:
                    #if it reaches how many books were found from query, cannot continue
                    if num_display == book_json["numFound"]:
                        break
                    book_cover.append("http://covers.openlibrary.org/b/id/"+str(book_json["docs"][num_display]["cover_i"])+"-L.jpg")
                    book_title.append(book_json["docs"][num_display]["title"])
                    num_display = num_display+1
                book_preview = zip(book_title, book_cover) #combine the lists to be able to display with loop
                context = {
                    "form_data": BooksForm(), #continue displaying form after searching
                    "book_preview": book_preview,
                }
                return render(request,'books/books.html', context)
    else:
        context = {
            "form_data": BooksForm(), #display form
        }
        return render(request, 'books/books.html', context)
