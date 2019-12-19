from django.urls import path, include
from . import views
from rest_framework.authtoken import views as token_views


urlpatterns = [
    path("", views.index, name="index"),
    path("post/new/", views.create_post, name="create_post"),
    path("post/update/<int:id>", views.update_post, name="update_post"),
    path("post/delete/<int:id>", views.delete_post, name="delete_post"),
    path("api/", include("posts.api.urls")),
]
