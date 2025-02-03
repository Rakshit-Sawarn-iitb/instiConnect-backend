from django.urls import path
from django.contrib import admin
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/",registration),
    path("",get_users_list),
    path("find_user/<name>", get_one_user),
    path("update/<id>", update),
    path("delete/<id>/", delete_account),
    path("follow/<id>", follow),
    path("sort_by_followers/", sort_by_followers),
    path("send_connection_request/", send_connection_request),
    path("accept_connection_request/",accept_connection_request),
    path("reject_connection_request/",reject_connection_request),
    path("get_all_requests/<id>",get_connection_requests),
    path("get_all_connections/<id>",get_connections),
    path("disconnect/",disconnect),
]
