from django.db import models
from django.contrib.auth.models import User



class PersonalInfo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	about_user = models.CharField(max_length=65536, null = True)
	personal_image = models.ImageField(null = True, blank = True)
	favorite_books = models.CharField(max_length=65536, null = True)

	#a follow model that just stores user id of people you follow
