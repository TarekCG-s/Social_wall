from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path("posts/", views.PostView, name="posts_api"),
]
