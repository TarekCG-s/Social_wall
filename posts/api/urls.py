from django.urls import path, include
from . import views


urlpatterns = [
    path("posts/", views.PostList.as_view()),
    path("posts/create/", views.CreatePostView.as_view()),
    path("posts/<pk>/", views.PostDetail.as_view()),
]
