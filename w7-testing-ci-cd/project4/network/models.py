from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

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