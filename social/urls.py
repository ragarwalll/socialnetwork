from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.index, name='index'),
    path('checkusername/', views.checkusername, name='checkusername'),
    path('home/', views.HomeView, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.UserLogout, name="logout"),
    path('forgot/', views.forgotpassword, name="forgotpassword"),
    re_path(r'like/(?P<pk>[0-9]+)/$', views.like, name="like"),
    re_path(r'comment/(?P<pk>[0-9]+)/$', views.comment, name="comment"),
    path('post/', views.post, name="post"),
]
