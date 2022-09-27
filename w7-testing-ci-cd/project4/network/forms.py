from django.db import models
from django.forms import ModelForm, Textarea
from .models import Post

class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        # Set form label to blank
        labels = {'body': ''}
        # Set HTML attrs for post body form
        widgets = {
            'body': Textarea(attrs={
                'cols': 80, 
                'rows': 2,
                'class': 'form-control border border-dark', 
                'placeholder': "What's up?",
                })
        }