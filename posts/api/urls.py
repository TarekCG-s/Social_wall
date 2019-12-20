from django.urls import path, include
from . import views


urlpatterns = [
    path("posts/", views.PostList.as_view(), name="api_all_posts"),
    path("posts/create/", views.CreatePostView.as_view(), name="api_create_post"),
    path("posts/<pk>/", views.PostDetail.as_view(), name="api_post_detail"),
]
