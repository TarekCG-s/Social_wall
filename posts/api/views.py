from rest_framework import generics
from posts.models import Post
from .serializers import PostSerializer


class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
