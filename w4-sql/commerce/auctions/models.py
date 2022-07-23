from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name="owner")
    listing_title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=12)
    image_url = models.URLField(max_length=2048, blank=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.id}"


class Bid(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, related_name="bidder")
    listing = models.ForeignKey(Listing, models.SET_NULL, null=True, related_name="bid_listing_id")
    bid = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
        related_name="commenter",
        )
    listing = models.ForeignKey(
        Listing,
        models.SET_NULL,
        null=True,
        related_name="comment_listing_id",
        )
    comment = models.CharField(max_length=75)

    def __str__(self):
        return f"{self.id}"