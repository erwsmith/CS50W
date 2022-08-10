from django import forms
from .models import *

class CreatePostForm(forms.Form):
    body = forms.CharField(label="", max_length=145, required=True)
    

# class BidForm(forms.Form):
#     bid = forms.DecimalField(label="", decimal_places=2, max_digits=12, required=True, min_value=0)


# class CommentForm(forms.Form):
#     comment = forms.CharField(label="", max_length=100, required=False)