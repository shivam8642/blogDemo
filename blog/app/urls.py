
from django.contrib import admin
from app import views
from django.urls import path,include

urlpatterns = [
    path('',views.index,name=''),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path("logout",views.logout,name="logout"),
    path('blog',views.blog,name='blog'),
    path('post_detail/<int:id>',views.post_detail,name='post_detail'),
    path('share_post/<int:id>/',views.share_post,name='share_post'),
    
   
]
