from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, EmailField, CharField, PasswordInput


class UserRegistrationForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(Form):
    username = CharField(label="Username")
    password = CharField(widget=PasswordInput)

