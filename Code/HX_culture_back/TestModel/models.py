# models.py
from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=20)

class Avatar(models.Model):
    user = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos', default='avatar.jpg')

class Image(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='static/form')#该函数需要安装第三方包pillow
