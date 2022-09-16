from django.db import models
from django.contrib.auth.models import User



class PersonalInfo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	about = models.CharField(max_length=65536, null = True)
	profile_pic = models.ImageField(null = True, blank = True)
	#list of friends
