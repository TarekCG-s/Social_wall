from django.forms import Form, ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
