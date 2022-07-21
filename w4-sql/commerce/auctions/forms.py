from django import forms


class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    description = forms.CharField(label="description", max_length=10000)
    starting_bid = forms.DecimalField(label="starting_bid", decimal_places=2, max_digits=12)
    image_url = forms.URLField(label="image_url", max_length=2048)
    category = forms.CharField(label="category", max_length=100)