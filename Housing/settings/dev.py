import django_on_heroku
from decouple import Config
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['mos-real.herokuapp.com']
SECRET_KEY = Config('SECRET_KEY')

django_on_heroku.settings(locals(),staticfiles=False)
del DATABASES['default']['OPTIONS']['sslmod']