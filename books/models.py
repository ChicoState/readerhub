from django.db import models
from django.contrib.auth.models import User

class BookReview(models.Model):#one per user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=100)
    text_review = models.CharField(max_length=65536)
    star_review = models.IntegerField()
	#can add book cover or other information if we need to access book info in other pages and dont want to query
