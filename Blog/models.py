from django.db import models
from django.conf import settings

# Create your models here.

class blog_catagory(models.Model):
 name = models.CharField(max_length=100)
 slug = models.SlugField(unique=True)

class blog(models.Model):
 title = models.CharField(max_length=100)
 catagory =models.ForeignKey(blog_catagory, on_delete=models.CASCADE)
 image = models.ImageField(upload_to='blog/',blank=True,null=True)
 description = models.TextField()
 auther =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 created = models.DateTimeField(auto_now_add=True)
 slug = models.SlugField(unique=True,blank=True,null=True)
 
 def __str__(self):
     return self.title
 