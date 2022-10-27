from django.db import models
from django.contrib.auth.models import User



class PersonalInfo(models.Model):#one per user
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	about_user = models.CharField(max_length=65536, null = True)
	personal_image = models.ImageField(null = True, blank = True)
	favorite_books = models.CharField(max_length=65536, null = True)

class FavoriteBooks(models.Model): #many to one relationship with User
	favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, default = "")
	favorite_books = models.CharField(max_length = 100)


class Follows(models.Model):#no implementation need to be able to follow with click
	current_user = models.ForeignKey(User, on_delete=models.CASCADE)
	follows = models.CharField(max_length=65536, null = True)
