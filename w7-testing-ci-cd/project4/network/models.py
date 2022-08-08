from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User", related_name="likedPosts")

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "user": self.user.username,
    #         "poster": self.poster.username,
    #         "likers": [user.email for user in self.likers.all()],
    #         "body": self.body,
    #         "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
    #     }

# class Like(models.Model):
#     user = models.ForeignKey(User, models.SET_NULL, null=True)
#     post = models.ForeignKey(Post, models.SET_NULL, null=True)
#     liked = models.BooleanField(models.SET_DEFAULT())

#     def __str__(self):
#         return f"{self.id}"


# class Follow(models.Model):
#     user = models.OneToOneField(User, models.SET_NULL, null=True, related_name="user_follow_list", unique=True)
#     follower = models.ManyToManyField(User, blank=True, related_name="follower")

#     def __str__(self):
#         return f"{self.id}"