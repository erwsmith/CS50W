from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.index, name="create"),
    path("edit", views.index, name="edit")
]
