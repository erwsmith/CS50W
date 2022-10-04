import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
        "active_user": request.user,
    })


def filtered_posts(request, post_view):
    if post_view == 'all':
        # Send all posts
        posts = Post.objects.all()
    elif post_view == 'following':
        # Send posts by users followed by active user
        active_user = User.objects.get(pk=request.user.id)
        active_user_as_follower = Follower.objects.get(user=active_user)
        posts = Post.objects.filter(user__in = active_user_as_follower.following.all())
    elif post_view == 'profile':
        # Send active user's posts
        profile_user = User.objects.get(pk=request.user.id)
        posts = Post.objects.filter(user=profile_user)
    else:
        return JsonResponse({"error": "Invalid filter."}, status=400)
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
def profile_view(request, username):
    profile_user = User.objects.get(username=username)
    active_user = User.objects.get(pk=request.user.id)
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
    
    # is_following = active_user_as_follower.following.filter(id=profile_user.id).exists()
    
    if request.method == "GET":
        try:
            profile_user = User.objects.get(username=username)
            posts = Post.objects.filter(user=profile_user)
            posts = posts.order_by("-timestamp").all()
            return JsonResponse([post.serialize() for post in posts], safe=False)
        except:
            return JsonResponse({"error": "Invalid filter."}, status=400)

    elif request.method == "PUT":

        data = json.loads(request.body) 
        
        if data.get("follow") is not None:
            if data.get("follow") == True:
                active_user_as_follower.following.add(profile_user)
                # messages.add_message(request, messages.SUCCESS, f"Following {profile_user}")
                return HttpResponse(status=204)
            elif data.get("follow") == False:
                active_user_as_follower.following.remove(profile_user)  
                # messages.add_message(request, messages.SUCCESS, f"Unfollowed {profile_user}")
                return HttpResponse(status=204)

    # Request method must be GET or PUT
    return JsonResponse({
        "error": "GET or PUT request required."
    }, status=400)


def get_followers(request, username):
    profile_user = User.objects.get(username=username)
    active_user = User.objects.get(pk=request.user.id)
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

    follower = follower.serialize()
    follower["is_following"] = active_user_as_follower.following.filter(id=profile_user.id).exists()
    return JsonResponse(follower, safe=False)


@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method == "PUT":
            data = json.loads(request.body)
            if data.get("like") is not None:
                try:
                    post = Post.objects.get(pk=post_id)
                except Post.DoesNotExist:
                    return JsonResponse({"error": "Post not found."}, status=404)
                if data.get("like") == True:
                    post.liked_by.add(data["liked_by"]) 
                    return HttpResponse(status=204)
                elif data.get("like") == False: 
                    post.liked_by.remove(data["unliked_by"])
                    return HttpResponse(status=204)
                post.save()
    return JsonResponse({"error": "PUT request required."}, status=400)


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
    return render(request, "network/register.html")
