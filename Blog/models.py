from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


# Create your models here.


class Catagoryes(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class blog(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    description = models.TextField()
    catagory = models.ForeignKey(
        Catagoryes, on_delete=models.SET_NULL, null=True, related_name='catagores')
    auther = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='blog_editor')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
