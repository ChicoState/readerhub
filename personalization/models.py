from django.db import models
from django.contrib.auth.models import User



class PersonalInfo(models.Model):#one per user
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	about_user = models.CharField(max_length=65536, null = True)
	personal_image = models.ImageField(null = True, blank = True)


class Follows(models.Model):
	user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
	following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
	#created = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		unique_together = ('user', 'following_user')

class FavoriteBooks(models.Model): #many to one relationship with User
	favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, default = "")
	favorite_books = models.CharField(max_length = 100)
