from codecs import lookup
import datetime
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Q
from cloudinary.models import CloudinaryField


# Create your models here.


class Conatct(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def blog_upload(instance, filename):
    file_path = 'Properte/{catagory}/{title}/-{filename}'.format(
        catagory=str(instance.catagory.name), title=str(instance.title),  filename=filename
    )


def uplaod_lucation(instance, filename):
    file_path = 'Properte/{proper}/-{filename}'.format(
        proper=str(instance.proper.title),  filename=filename
    )
    return file_path


def uplaod_lucationn(instance, filename):
    file_path = 'Properte/{proper}/-{filename}'.format(
        proper=str(instance.title),  filename=filename
    )
    return file_path


class aria(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Rent(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class House(models.Model):
    RENT_CHOICHES = [
        ('سنة', 'سنة'),
        ('شهر', 'شهر'),
        ('أسبوع', 'أسبوع'),
        ('يوم', 'يوم'),
    ]

    title = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    building_type = models.ForeignKey(
        Building, on_delete=models.CASCADE, blank=True, null=True)
    num_rooms = models.IntegerField(blank=True, null=True)
    rent_type = models.ForeignKey(
        Rent, on_delete=models.SET_NULL, blank=True, null=True)
    aria = models.ForeignKey(
        aria, on_delete=models.SET_NULL, null=True, related_name='place')
    created = models.DateTimeField(auto_now_add=True)
    space = models.IntegerField(blank=True, null=True)
    favourties = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='favourties', default=None, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    status = models.BooleanField(default=True)
    cover = CloudinaryField('image')
    property_type = models.ForeignKey(
        Purpose, on_delete=models.SET_NULL, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    lati = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    Agent = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, null=True, blank=True)
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='property_editor')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.property_type.name}'


class extras(models.Model):
    name = models.CharField(max_length=100)
    proper = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class galary(models.Model):
    image = CloudinaryField('image')
    proper = models.ForeignKey(House, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    proper = models.ForeignKey(House, on_delete=models.CASCADE)
    messaage = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey(
        'self', blank=True, null=True, related_name='replays', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.messaage} By {self.user.username}"

    @property
    def is_parent(self):
        if self.parent_id is not None:
            return False
        return True


class Testomany(models.Model):
    REVIEW_CHOICHES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    review = models.IntegerField(choices=REVIEW_CHOICHES, default=2)

    def __str__(self):
        return f'{self.name} give {self.review}'
