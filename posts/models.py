from django.db import models
from django.contrib.auth.models import User
from personalization.models import FavoriteBooks
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_object = models.ForeignKey(FavoriteBooks, on_delete=models.CASCADE)#added null = true to not have to redo migrations
    # created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_modified"]

    def __str__(self):
        return self.title
