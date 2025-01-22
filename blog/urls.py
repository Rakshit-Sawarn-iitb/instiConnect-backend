from django.urls import path
from django.contrib import admin

from .views import *

urlpatterns = [
    path('', get_many_blog, name='get_all'),
    path('post/', post_blog, name='post_blog_'),
    path('find/' , get_one_blog , name = 'get_one'),
    path('delete/' , delete_blog , name = 'delete'),
    path('find/' , get_one_blog , name = 'get_one'),
    path('like/' , like_blog , name = 'like'),   
    
]