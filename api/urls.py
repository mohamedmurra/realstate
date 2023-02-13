
from django.urls import path, re_path
from .views import admin_blog_view, favo_add, favo_remove, galary_view, house_view, get_house, get_blog, Testemonay_view, Purpose_view, aria_view, add_info_view, homepage_view, blog_view, Teammember, Agent_detail, Add_coment_view, Searsh_filter, MyTokenObtainPairView, BlackListTokenView, ContactView, user_detail, admin_view, add_house_view, add_blog_view, blog_catagory_view, favourties_view, Dashbord_view, users, users_update, update_house, admin_house_view, update_blog, admin_house_images, add_building, get_images_view, house_view_all, Register_by_Acsses_token

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view()),
    path('logout/blacklist/', BlackListTokenView.as_view()),
    path('home/', house_view.as_view()),
    path('home/all/', house_view_all.as_view()),
    path('home/admin/', admin_house_view.as_view()),
    path('home/admin/images/', admin_house_images.as_view()),
    path('home/admin/get_images/<id>/', get_images_view),
    path('blog/admin/', admin_blog_view.as_view()),
    path('dashbord/', Dashbord_view),
    path('dashbord/users/', users.as_view()),
    path('dashbord/users/<id>/', users_update.as_view()),
    path('blog/', blog_view.as_view()),
    path('contact/', ContactView.as_view()),
    path('admin/contact/', admin_view),
    path('homepage/', homepage_view),
    path('home/property/<slug>/', get_house.as_view()),
    path('home/property/update/<slug>/', update_house.as_view()),
    path('home/comment/', Add_coment_view.as_view()),
    path('blog/<slug>/', get_blog.as_view()),
    path('blog/update/<slug>/', update_blog.as_view()),
    path('Testemony/', Testemonay_view.as_view()),
    path('home/searsh-filter/', Searsh_filter),
    path('home/add-images/', galary_view.as_view()),
    path('home/blog-catagory/', blog_catagory_view.as_view()),
    path('home/add-house/', add_house_view.as_view()),
    path('home/add-blog/', add_blog_view.as_view()),
    path('home/Purpose/', Purpose_view.as_view()),
    path('home/aria/', aria_view.as_view()),
    path('home/building/', add_building.as_view()),
    path('home/fav/', favourties_view.as_view()),
    path('home/fav/add/', favo_add.as_view()),
    path('home/fav/remove/', favo_remove.as_view()),
    path('home/add-info/', add_info_view.as_view()),
    path('home/profile/<str:id>/', user_detail.as_view()),
    path('TeamMember/', Teammember.as_view()),
    path('TeamMember/agent-detail/<str:id>/', Agent_detail.as_view()),
    re_path('social_register/' +
            r'social/(?P<backend>[^/]+)/$', Register_by_Acsses_token)
]
