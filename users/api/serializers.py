from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ["id", "username", "posts"]


class RegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = User(
            username=self.validated_data["username"], email=self.validated_data["email"]
        )
        password = self.validated_data["password"]
        if len(password) < 8:
            raise serializers.ValidationError({"Error":"Password must be longer than 8 characters"})
        user.set_password(password)
        user.save()
