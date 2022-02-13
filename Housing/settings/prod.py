import django_on_heroku
from decouple import Config
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['realstate-sd.herokuapp.com']
SECRET_KEY = Config('SECRET_KEY')