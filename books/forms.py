# pylint: disable=C0114, C0115, E5142
from django import forms
from books.models import BookReview


class BooksForm(forms.Form):
    book_search = forms.CharField()

class BookReviewForm(forms.ModelForm):
    text_review = forms.CharField(widget=forms.Textarea(attrs={'rows': '9' , 'cols': '80'}))
    CHOICES = [(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')] #star rating out of 5
    star_review = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect())

    class Meta():
        model = BookReview
        fields = ['text_review']
