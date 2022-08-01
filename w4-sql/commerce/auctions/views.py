from operator import is_
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max, Count

from .models import User, Listing, Bid, Comment, Category, Watchlist
from .forms import BidForm, CreateEntryForm, CommentForm


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


def watchlist_view(request):
    try:
        watchlist = Watchlist.objects.get(user=int(request.user.id))
        return render(request, "auctions/watchlist_view.html", {
            "listings": watchlist.listings.all()
            })
    except:
        messages.info(request, "Your watchlist is currently empty.")
        return render(request, "auctions/watchlist_view.html")


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by('category_name')
        })


def category_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category_view.html", {
        "category": category,
        "listings": category.category_listings.all(),
    })


def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        category = Category.objects.get(category_name=listing.category)
    except:
        category = 0
    comments = Comment.objects.filter(listing__id=listing_id)

    # TODO identify winner of auction
    # Get all bids associated with listing
    bids = Bid.objects.filter(listing__id=listing_id)
    # Count number of bids
    bid_count = bids.aggregate(Count('bid'))['bid__count']
    # Get max bid
    try:
        bid_max = f"${bids.aggregate(Max('bid'))['bid__max']:,.2f}"
    except:
        bid_max = listing.starting_bid
    # Get max bidder
    try:
        highest_bidder = bids.order_by('-bid')[0].user
    except:
        highest_bidder = "No bids"

    if request.method == "POST":
        # Watchlist handling
        # Add to watchlist
        if "watchlist_button" in request.POST:
            # If user has a watchlist already
            try:
                watchlist = Watchlist.objects.get(user=int(request.user.id))
                watchlist.listings.add(listing)
                messages.success(request, "Listing added to your watchlist!")
                return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
            # If user does not have a watchlist yet
            except:
                watchlist = Watchlist(user=User.objects.get(pk=int(request.user.id)))
                watchlist.save()
                watchlist.listings.add(listing)
                messages.success(request, "New watchlist created and listing added!")
                return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        # Remove from watchlist
        elif "rm_watchlist_button" in request.POST:
            watchlist = Watchlist.objects.get(user=int(request.user.id))
            watchlist.listings.remove(listing)
            messages.success(request, "Listing removed from watchlist")
            return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        # Close auction
        elif "close_button" in request.POST:
            listing.status = "closed"
            listing.save()
            messages.success(request, "Auction closed")
            return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        # Post comment
        elif "comment_form" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                c = Comment(
                user = User.objects.get(pk=int(request.user.id)),
                listing = listing,
                comment = comment_form.cleaned_data["comment"]
                )
                c.save()
                messages.success(request, "Comment posted!")
                return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        # Bid handling
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            b = Bid(
                user = User.objects.get(pk=int(request.user.id)),
                listing = listing,
                bid = bid_form.cleaned_data["bid"]
                )
            if b.bid > listing.current_price:
                b.save()
                listing.current_price = b.bid
                listing.save()
                listing = Listing.objects.get(pk=listing_id)
                messages.success(request, "Your bid was successful!")
                return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
            messages.warning(request, "Bid is too low.")
            return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
        messages.warning(request, "Invalid form.")
        return HttpResponseRedirect(reverse("listing_view", args=(listing.id,)))
    # GET request method handling
    # Check if listing is in user's watchlist
    watchlist_button = "add"
    try: 
        watchlist = Watchlist.objects.get(user=int(request.user.id))
        if listing in watchlist.listings.all():
            watchlist_button = "remove" 
    except:
        pass
    return render(request, "auctions/listing_view.html", {
        "listing": listing,
        "category":category,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "watchlist_button": watchlist_button,
        "bid_count": bid_count,
        "bid_max": bid_max, 
        "bids": bids, 
        "highest_bidder": highest_bidder,
        "comments": comments
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


def closed_listings(request):
    '''This page shows all closed listings'''
    return render(request, "auctions/closed_listings.html", {
        "listings": Listing.objects.all()
        })