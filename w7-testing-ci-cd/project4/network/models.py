from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False, max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, blank=True, related_name="likers")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "liked_by": [user.username for user in self.liked_by.all()], 
        }

    def __str__(self):
        return f"{self.id}"

class Like(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    post = models.ForeignKey(Post, models.SET_NULL, null=True, related_name="likes")
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

class Follower(models.Model):
    user = models.OneToOneField(User, models.SET_NULL, null=True)
    following = models.ManyToManyField(User, blank=True, related_name="followers")

    def is_valid_follower(self):
        return self.user not in self.following.all()

    def __str__(self):
        return f"{self.id}"