from .base import *
from decouple import Config


DEBUG = True

ALLOWED_HOSTS = ['*']
SECRET_KEY = Config('SECRET_KEY')