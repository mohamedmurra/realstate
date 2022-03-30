from django.db import models
from django.conf import settings

# Create your models here.


class Catagory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __Str__(self):
        return self.name


class blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    description = models.TextField()
    catagoey = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, blank=True, null=True)
    auther = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title
