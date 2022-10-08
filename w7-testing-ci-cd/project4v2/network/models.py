from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False, max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "user_id": self.user.id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": [user.username for user in self.liked_by.all()],
            "likes_count": self.liked_by.count(),
        }

    def __str__(self):
        return f"{self.id}"

class Follower(models.Model):
    user = models.OneToOneField(User, models.SET_NULL, null=True)
    following = models.ManyToManyField(User, blank=True, related_name="followers")

    def is_valid_follower(self):
        return self.user not in self.following.all()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "user_id": self.user.id,
            "following": [user.username for user in self.following.all()],
            "following_count": self.following.count(),
            "followers_count": self.user.followers.count(),
        }

    def __str__(self):
        return f"{self.id}"