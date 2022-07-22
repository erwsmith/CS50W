from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # username, email, password
    pass

class Listing(models.Model):
    listing_title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=12)
    image_url = models.URLField(max_length=2048)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}: {self.listing_title}"

# class Bids():
#     pass

# class Comments():
#     pass