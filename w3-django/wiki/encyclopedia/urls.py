from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("searchResult", views.searchResult, name="searchResult"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit")
]