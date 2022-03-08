from django.urls import path
from . import views

urlpatterns = [
 path('',views.homepage,name='homepage'),
 path('property/<slug>',views.property_detail,name='property-detail'),
 path('property/',views.propertes,name='property'),
 path('agent/',views.agents,name='agents'),
 path('agent/<slug>',views.agent,name='agent_detail'),
 path('login/',views.login_view ,name='login'),
 path('about/',views.about ,name='about'),
 path('contact/',views.contact ,name='contact'),
 path('dashbord/', views.dashbord, name='dashbord'),
 path('dashbord/properys/', views.propertes, name='properts'),
 path('dashbord/profile/', views.admin_settigns, name='profile'),
 path('dashbord/properys/searsh', views.searsh_property, name='searsh_properts'),
 path('dashbord/add-images/', views.add_house_image, name='add_images'),
 path('dashbord/add-info/<slug>', views.add_house_info, name='add_info'),
 path('dashbord/add-blog/', views.add_blog, name='add_blog'),
 path('dashbord/add-property/', views.add_property, name='add_property'),
 path('dashbord/update-property/<slug>/', views.update_property, name='update_property'),
 path('dashbord/delete-property/<slug>/',
      views.delete_property, name='delete_property'),
 path('dashbord/blogs/', views.all_blog, name='blogs_manager'),
 path('dashbord/blogs/add/', views.add_blog, name='add_blog'),
 path('dashbord/blogs/update/<slug>', views.update_blog, name='update_blog'),
 path('dashbord/blogs/delete/<slug>', views.delete_blog, name='delete_blog'),
 path('searsh/',views.searsh_header ,name='searsh'),
 path('register/',views.register_view,name='register'),
 path('logout/',views.logout_view ,name='logout')
]
