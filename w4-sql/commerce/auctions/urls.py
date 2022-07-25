from django.urls import path

from . import views

# URL Conf
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("<str:category>", views.category, name="category"),
    path("<str:username>/create_listing/", views.create_listing, name="create_listing"),
    path("<int:listing_id>/", views.listing, name="listing"), 
]