from django.urls import path

# get views.py from current directory
from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("<str:name>", views.greet, name="greet"),
    path("eric", views.eric, name="eric")
]

