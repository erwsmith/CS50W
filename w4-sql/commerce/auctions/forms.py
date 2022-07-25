from django import forms

from .models import Category

class CreateEntryForm(forms.Form):
    listing_title = forms.CharField(label="Title", max_length=100, required=True)
    description = forms.CharField(label="description", max_length=10000, required=True)
    starting_bid = forms.DecimalField(label="starting_bid", decimal_places=2, max_digits=12, required=True)
    image_url = forms.URLField(label="image_url", max_length=2048, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=False)


class BidForm(forms.Form):
    bid = forms.DecimalField(label="bid", decimal_places=2, max_digits=12, required=True)


# class Watchlist(forms.Form):
#     pass