from django.contrib import admin

from .models import Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "description", "starting_bid", "category") 

# use ListingAdmin settings with Listing
admin.site.register(Listing, ListingAdmin)
