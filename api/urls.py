
from django.db import router
from django.urls import path
from .views import house_view, get_house, blog_view, get_blog

urlpatterns = [
    path('home', house_view.as_view()),
    path('home/<int:id>/', get_house.as_view()),
    path('blog/', blog_view.as_view()),
    path('blog/<int:id>', get_blog.as_view()),
]
