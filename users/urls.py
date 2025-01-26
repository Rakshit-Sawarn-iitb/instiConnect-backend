from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    path("register/",registration),
    path("",get_users_list),
    path("find_user/<id>", get_one_user),
    path("update/<id>", update),
    path("delete/<id>/", delete_account),
    path("follow/<id>", follow),
    path("sort_by_followers", sort_by_followers),
]
