from django.db import models
from django.forms import ModelForm, Textarea
from .models import Post

class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': Textarea(attrs={
                'cols': 80, 
                'rows': 2,
                'class': 'form-control border border-light', 
                'placeholder': "What's up?",
                })
        }