from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Listing, Bid, Comment, Category, Watchlist

# Django Admin Settings
class ListingAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "user", "description", "starting_bid", "current_price", "category", "id")
    ordering = ["user"]

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "bid", "id")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("comment", "user", "listing", "id")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "id")
    ordering = ["category_name"]

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "id")
    ordering = ["user"]
    filter_horizontal = ("listings",)


# Model registration
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)