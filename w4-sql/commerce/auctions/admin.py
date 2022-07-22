from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "description", "starting_bid", "category") 

# use ListingAdmin settings with Listing
admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)