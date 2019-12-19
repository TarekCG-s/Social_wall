from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegistrationForm, UserLoginForm


# Registeration View
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            mail_data = {
                "subject": "Welcome To Social_Wall",
                "body": f"Thank You {username} for joining us.",
                "from": "Social Wall",
                "to": [email],
            }
            send_mail(
                mail_data["subject"],
                mail_data["body"],
                mail_data["from"],
                mail_data["to"],
                fail_silently=False,
            )
            login(request, user)
            messages.success(request, f"Thank {username} for making an account")
            return redirect("index")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "users/register.html", context=context)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Wlcome Back {username}")
                return redirect("index")
            else:
                messages.error(request, "You entered an invalid username or password")
    context = {
        "form": form,
    }
    return render(request, "users/login.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("index")
