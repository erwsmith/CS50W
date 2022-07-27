from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category, Watchlist
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
            messages.success(request, "Login successful")
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/login.html")
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Log out successful.")
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request, "Passwords must match.")
            return render(request, "auctions/register.html")
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")


def watchlist_view(request, user_id):
    try:
        watchlist = Watchlist.objects.get(user=user_id)
        return render(request, "auctions/watchlist_view.html", {
            "listings": watchlist.listings.all()
            })
    except:
        messages.info(request, "Your watchlist is currently empty.")
        return render(request, "auctions/watchlist_view.html")


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
        })


def category_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category_view.html", {
        "category": category,
        "listings": category.category_listings.all()
    })


def listing_view(request, listing_id):
    if request.method == "POST":
        if "watchlist_button" in request.POST:
            listing = Listing.objects.get(pk=listing_id)
            category = Category.objects.get(category_name=listing.category)
            try:
                # THIS NEEDS TO BE FIXED, IT'S MAKING A NEW WATCHLIST EVERY TIME
                watchlist = Watchlist.objects.get(pk=int(request.user.id))
                watchlist.listings.add(listing)
                messages.success(request, "Listing added to your watchlist.")
                return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
            except:
                watchlist = Watchlist(
                    user = User.objects.get(pk=int(request.user.id)),
                )
                watchlist.save()
                watchlist.listings.add(listing)
                messages.info(request, "New watchlist created.")
                return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        
        form = BidForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(pk=listing_id)
            b = Bid(
                user = User.objects.get(pk=int(request.user.id)),
                listing = listing,
                bid = form.cleaned_data["bid"]
                )
            bid_value = b.bid
            if bid_value > listing.current_price:
                b.save()
                listing.current_price = bid_value
                listing.save()
                listing = Listing.objects.get(pk=listing_id)
                category = Category.objects.get(category_name=listing.category)
                messages.success(request, "Your bid was successful!")
                return render(request, "auctions/listing_view.html", {
                    "listing": listing,
                    "category":category,
                    "form": BidForm(),
                })
            return HttpResponse("bid is too low")
        return HttpResponse("invalid form")
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
            messages.success(request, "Listing created!")
            return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        return HttpResponse("invalid form")
    return render(request, "auctions/create_listing.html", {
        "form": CreateEntryForm()
    })