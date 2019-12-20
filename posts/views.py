from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User


def index(request):
    posts_all = Post.objects.all()
    paginator = Paginator(posts_all, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "posts": posts,
        "page": page,
    }
    return render(request, template_name="posts/index.html", context=context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(
                request,
                f"Thank you {request.user.username}. Your post has been published",
            )
            return redirect("index")
        else:
            messages.error(
                request,
                f"Sorry {request.user.username}. There's an error in your post.",
            )
    context = {"form": form}
    return render(request, "posts/create_post.html", context=context)


@login_required
def update_post(request, id):

    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return render(request, "posts/error.html", {"message": "There's no such post"})

    if post.author.id != request.user.id:
        return render(
            request, "posts/error.html", {"message": "You can't update that post"}
        )

    form = PostForm(
        request.POST or None,
        instance=post,
        initial={"title": post.title, "content": post.content},
    )
    if request.method == "POST":
        if form.is_valid:
            form.save()
            messages.success(
                request, "Your post has been updated",
            )
            return redirect("index")
        else:
            messages.error(
                request,
                f"Sorry {request.user.username}. There's an error in your post.",
            )

    context = {"form": form}
    return render(request, "posts/update_post.html", context=context)


@login_required
def delete_post(request, id):

    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return render(request, "posts/error.html", {"message": "There's no such post"})
    if post.author.id != request.user.id:
        return render(
            request, "posts/error.html", {"message": "You can't delete that post"}
        )
    else:
        post.delete()
        messages.success(
            request, "Your post has been deleted",
        )

    return redirect("index")

