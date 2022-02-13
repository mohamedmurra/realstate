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
 path('add-property/',views.add_house ,name='add_house'),
 path('searsh/',views.searsh_header ,name='searsh'),
 path('register/',views.register_view,name='register'),
 path('logout/',views.logout_view ,name='logout')
]
