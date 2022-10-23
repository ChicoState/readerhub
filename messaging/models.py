from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    content = models.CharField(max_length=65536, null = False)
    sent_at = models.DateTimeField(auto_now_add = True)