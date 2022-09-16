#from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User as auth_user

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

class Profile(models.Model):
    user = models.OneToOneField(auth_user, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    follows = models.ManyToManyField("self", symmetrical=True, blank=True)

    def __str__(self):
        return self.name