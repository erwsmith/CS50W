# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# # Django Admin Settings
# class EmailAdmin(admin.ModelAdmin):
#     list_display = ("user", "sender", "subject", "timestamp", "read", "archived", "id")
#     ordering = ["user"]

# Model registration
admin.site.register(User, UserAdmin)
