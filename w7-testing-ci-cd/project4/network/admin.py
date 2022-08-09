# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post, Like, Follower

# Django Admin Settings
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "body", "timestamp", "id")
    ordering = ["user"]

class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "liked", "id")
    ordering = ["user"]

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("user", "id")
    ordering = ["user"]

# Model registration
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follower, FollowerAdmin)