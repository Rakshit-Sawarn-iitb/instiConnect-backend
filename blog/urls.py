from django.urls import path
from django.contrib import admin

from .views import *

urlpatterns = [
    path('', get_many_blog, name='get_all'),
    path('post/', post_blog, name='post_blog_'),
    path('find/' , get_one_blog , name = 'get_one'),
    path('delete/' , delete_blog , name = 'delete'),
    path('delete/<int:id>/' , delete_blog , name = 'delete'),
    path('find/' , get_one_blog , name = 'get_one'),
    path('find/<int:id>/' , get_one_blog , name = 'get_one'),
    path('like/' , like_blog , name = 'like'),
    path('like/<int:id>/', like_blog, name='like_blog'),
    path('edit/<int:id>/', edit_blog, name='edit_blog'),

    
]