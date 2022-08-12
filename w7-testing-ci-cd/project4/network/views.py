from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import *
from .models import *


def index(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            # Create new post object with form data
            post = Post(
                user=User.objects.get(username=request.user.username),
                body=form.cleaned_data["body"],
            )
            # Save the above as a new post in the database
            post.save()
            messages.success(request, "Post created!")
            return HttpResponseRedirect(reverse("index"))
        return HttpResponse("invalid form")
    posts = list(Post.objects.all().order_by('-timestamp'))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "form": CreatePostForm(), 
        "page_obj": page_obj,
    })


def following_view(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            # Create new post object with form data
            post = Post(
                user=User.objects.get(username=request.user.username),
                body=form.cleaned_data["body"],
            )
            post.save()
            messages.success(request, "Post created!")
            return HttpResponseRedirect(reverse("index"))
        return HttpResponse("invalid form")
    active_user = User.objects.get(pk=request.user.id)
    active_user_as_follower = Follower.objects.get(user=active_user)
    following_posts = list(Post.objects.filter(user__in = active_user_as_follower.following.all()).order_by('-timestamp'))
    return render(request, "network/following_view.html", {
        "form": CreatePostForm(), 
        "posts": following_posts,
    })


def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    active_user = User.objects.get(pk=request.user.id)
    # check if profile_user has a follower object yet, if not, create one
    try: 
        follower = Follower.objects.get(user=profile_user)
    except: 
        Follower.objects.create(user=profile_user)
        follower = Follower.objects.get(user=profile_user)
    # check if active_user has a follower object yet, if not, create one
    try: 
        active_user_as_follower = Follower.objects.get(user=active_user)
    except: 
        Follower.objects.create(user=active_user)
        active_user_as_follower = Follower.objects.get(user=active_user)
    posts = Post.objects.filter(user=user_id).order_by('-timestamp')
    is_following = active_user_as_follower.following.filter(id=profile_user.id).exists()
    if request.method == "POST":
        if "follow-button" in request.POST:
            active_user_as_follower.following.add(profile_user)
            messages.success(request, f"Following {profile_user}")
            return HttpResponseRedirect(reverse("profile", args=(user_id,)))
        if "unfollow-button" in request.POST:
            active_user_as_follower.following.remove(profile_user)
            messages.success(request, f"Unfollowed {profile_user}")
            return HttpResponseRedirect(reverse("profile", args=(user_id,)))
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
        "follower": follower,
    })


# def posts_display(request, display):
#     # Filter posts returned based on display
#     if display == "profile":
#         posts = Post.objects.filter(user=request.user)
#     elif display == "all":
#         posts = Post.objects.all()
#     elif display == "following":
#         posts = Post.objects.all()
#         # posts = Post.objects.filter(user=request.user.following.all())
#     else:
#         return JsonResponse({"error": "Invalid display requested."}, status=400)

#     # Return posts in reverse chronologial order
#     posts = posts.order_by("-timestamp").all()
#     return JsonResponse([post.serialize() for post in posts], safe=False)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
