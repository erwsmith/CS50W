from django.urls import path

from . import views

# URL Conf
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view"),
    path("<int:category_id>/", views.category_view, name="category_view"),
    path("closed_listings/", views.closed_listings, name="closed_listings"),
    path("<int:listing_id>/listing_view", views.listing_view, name="listing_view"), 
    path("<str:username>/create_listing/", views.create_listing, name="create_listing"),
]