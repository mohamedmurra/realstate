
from cgitb import lookup
from rest_framework import mixins
from django.shortcuts import get_object_or_404, render
from .serializers import Housing_serlizer
from rest_framework import generics
from Main.models import House
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from Blog.models import blog
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# Create your views here.


class house_view(generics.ListCreateAPIView):
    serializer_class = Housing_serlizer
    queryset = House.objects.all()
    authentication_class = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class get_house(generics.RetrieveAPIView):
    serializer_class = Housing_serlizer
    queryset = House.objects.all()
    lookup_field = 'id'


class blog_view(generics.ListAPIView):
    serializer_class = Housing_serlizer
    queryset = blog.objects.all()


class get_blog(generics.RetrieveAPIView):
    serializer_class = Housing_serlizer
    queryset = blog.objects.all()
    lookup_field = 'id'
