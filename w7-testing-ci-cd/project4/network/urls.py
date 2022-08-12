
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("following_view/", views.following_view, name="following_view"),
    path("<int:user_id>/profile/", views.profile, name="profile"),
]