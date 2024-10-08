import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from cloudinary.models import CloudinaryField

# Create your models here.


def uplaod_lucation(instance, filename):
    file_path = 'Acount/{email}/{username}-{filename}'.format(
        email=str(instance.email), username=str(instance.username), filename=filename
    )
    return file_path


USER_CHOICES = (
    ('ADMIN', 'ADMIN'),
    ('STAFF', 'STAFF'),
    ('AGENT', 'AGENT'),
    ('CUSTOMER', 'CUSTOMER')
)


class Acount_Manger(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('user must have email')
        if not username:
            raise ValueError('user must have username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    REQUIRED_FIELDS = ['username', ]

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Acount(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICHES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=20, unique=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICHES, blank=True, null=True)
    user_type = models.CharField(
        max_length=10, choices=USER_CHOICES, default='CUSTOMER')
    first_name = models.CharField(max_length=50, blank=True, null=True, )
    last_name = models.CharField(max_length=50, blank=True, null=True, )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatssap = models.IntegerField(blank=True, null=True, )
    describe = models.TextField(blank=True, null=True)
    image = CloudinaryField('image')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = Acount_Manger()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


def Code_genrater():
    length = 5
    code = ''.join(random.choices(string.hexdigits, k=length))
    return code


