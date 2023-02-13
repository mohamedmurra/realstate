from django.shortcuts import render
from social_core.backends import google


def React(request):
    return render(request, 'index.html')


class GoogleOAuth2(google.GoogleOAuth2):
    STATE_PARAMETER = False
