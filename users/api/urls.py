from django.urls import path, include
from . import views
from rest_framework.authtoken import views as token_views


urlpatterns = [
    path("users/", views.UserList.as_view()),
    path("users/create/", views.CreateUserView.as_view()),
    path("users/<pk>/", views.UserDetail.as_view()),
    path("auth/", include("rest_framework.urls")),
    path("token/", token_views.obtain_auth_token),
]
