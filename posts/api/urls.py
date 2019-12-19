from django.urls import path, include
from . import views
from rest_framework.authtoken import views as token_views


urlpatterns = [
    path("posts/", views.PostList.as_view()),
    path("posts/create/", views.CreatePostView.as_view()),
    path("posts/<pk>/", views.PostDetail.as_view()),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    path("auth/", include("rest_framework.urls")),
    path("token/auth/", token_views.obtain_auth_token),
]
