from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Listing, Bid, Comment

# Django Admin Settings
class ListingAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "user", "description", "starting_bid", "category", "id") 

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "bid", "id")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "user", "listing", "id")


# Model registration
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)