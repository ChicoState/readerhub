#from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User as auth_user

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    #vote count
    #book "tag"? potentially

    def __str__(self):
        return self.body

class Profile(models.Model):
    user = models.OneToOneField(auth_user, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    #follows = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.name

class Follows(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    username = models.CharField(Profile.name, max_length=50)

    def __str__(self):
        return self.username