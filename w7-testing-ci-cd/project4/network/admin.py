# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post, Follower

# Django Admin Settings
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "id")
    ordering = ["id"]

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "body", "timestamp", "id")
    ordering = ["user"]
    filter_horizontal = ("liked_by",)

class FollowerAdmin(admin.ModelAdmin):
    list_display = ("user", "id")
    ordering = ["user"]
    filter_horizontal = ("following",)

# Model registration
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follower, FollowerAdmin)