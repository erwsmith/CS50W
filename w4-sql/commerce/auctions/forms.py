from django import forms

from .models import Category

class CreateEntryForm(forms.Form):
    listing_title = forms.CharField(label="Title", max_length=100, required=True)
    description = forms.CharField(label="Description", max_length=10000, required=True)
    starting_bid = forms.DecimalField(label="Starting Bid", decimal_places=2, max_digits=12, required=True)
    image_url = forms.URLField(label="Image URL", max_length=2048, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=False)


class BidForm(forms.Form):
    bid = forms.DecimalField(label="", decimal_places=2, max_digits=12, required=True, min_value=0)


class CommentForm(forms.Form):
    comment = forms.CharField(label="", max_length=100, required=False)