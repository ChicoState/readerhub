# pylint: disable=C0114, C0115, E5142
from django.db import models
from app1.models import Activity

class BookReview(Activity):#one per book
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=100)
    text_review = models.CharField(max_length=65536)
    star_review = models.IntegerField()
    book_title = models.CharField(max_length=100)
    book_cover = models.CharField(max_length=100)
