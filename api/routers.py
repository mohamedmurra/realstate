from rest_framework.routers import DefaultRouter
from .viewsset import admin_images_viewsets, Profile_viewset, Messages, users, admin_info_viewsets


router = DefaultRouter()
router.register('images', admin_images_viewsets, basename='images')
router.register('extra', admin_info_viewsets, basename='extra')
router.register('profile', Profile_viewset, basename='profile')
router.register('users', users, basename='users')
router.register('messages', Messages, basename='messages')

urlpatterns = router.urls
