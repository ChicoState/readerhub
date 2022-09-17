from django.db import models

# Create your models here.
class Books(models.Model):
    isbn = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    yop = models.IntegerField()
    publisher = models.CharField(max_length=200)
    imgUrlS = models.URLField()
    imgUrlM = models.URLField()
    imgUrlL = models.URLField()

    def __str__(self):
        return self.title