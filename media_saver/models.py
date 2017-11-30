from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to= "", default='pic_folder/None/no-img.jpg')
    file = models.FileField(upload_to="", default='pic_folder/None/no-img.mp4')
    url = models.CharField(max_length=400)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    mtype = models.IntegerField() #0 - photo  1 - video

class SocialAccount(models.Model):
    instagram = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)