from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.v1 import views

urlpatterns = [
    path(
        "create/",
        views.ProfileCreateView.as_view(),
        name="profile_create",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "login/refresh/",
        TokenRefreshView.as_view(),
        name="refresh_token",
    ),
    path(
        "<username>/",
        views.ProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path(
        "<username>/followers/",
        views.ProfileFollowersView.as_view(),
        name="profile_followers",
    ),
]
