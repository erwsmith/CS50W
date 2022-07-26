from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category
from .forms import BidForm, CreateEntryForm


def index(request):
    '''This page shows all active listings'''
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html")


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })


def category_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category_view.html", {
        "category": category,
        "listings": category.category_listings.all()
    })


def listing_view(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            b = Bid(bid=form.cleaned_data["bid"])
            b.save()
        else:
            return HttpResponse("invalid form")
    else:
        listing = Listing.objects.get(pk=listing_id)
        category = Category.objects.get(category_name=listing.category)
        return render(request, "auctions/listing_view.html", {
            "listing": listing,
            "category":category,
            "form": BidForm(),
        })


def create_listing(request, username):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            # Create new listing object with form data
            listing = Listing(
                user = User.objects.get(username=username),
                listing_title = form.cleaned_data["listing_title"],
                description = form.cleaned_data["description"],
                starting_bid = form.cleaned_data["starting_bid"],
                current_price = form.cleaned_data["starting_bid"],
                image_url = form.cleaned_data["image_url"],
                category = form.cleaned_data["category"]
            )
            # Save the above as a new listing in the database
            listing.save()
            return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        else:
            return HttpResponse("invalid form")
    else:
        return render(request, "auctions/create_listing.html", {
            "form": CreateEntryForm()
        })