from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # username, email, password
    pass

class Listing(models.Model):
    title = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    description = models.CharField(max_length=10000)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=12)
    image_url = models.URLField(max_length=2048)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}: {self.title}"

# class Bids():
#     pass

# class Comments():
#     pass