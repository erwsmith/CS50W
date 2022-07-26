from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.category_name}"


class Listing(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name="owner")
    listing_title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=12)
    current_price = models.DecimalField(decimal_places=2, max_digits=12)
    image_url = models.URLField(max_length=2048, blank=True)
    category = models.ForeignKey(Category, models.SET_NULL, null=True, related_name="category_listings", blank=True)

    def __str__(self):
        return f"{self.listing_title}"


class Bid(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name="bidder")
    listing = models.ForeignKey(Listing, models.SET_NULL, null=True, related_name="bid_listing_id")
    bid = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f"{self.id}"


class Watchlist(models.Model):
    user = models.OneToOneField(User, models.SET_NULL, null=True, related_name="user_watchlist", unique=True)
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlist_listing_id")

    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name="commenter",)
    listing = models.ForeignKey(Listing, models.SET_NULL, null=True, related_name="comment_listing_id",)
    comment = models.CharField(max_length=75)

    def __str__(self):
        return f"{self.id}"