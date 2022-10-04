from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # API Routes
    path("posts/<str:post_view>", views.filtered_posts, name="filtered_posts"),
    path("profile/<str:username>", views.profile_view, name="profile_view"),
    path("followers/<str:username>", views.get_followers, name="get_followers"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
]