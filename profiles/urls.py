from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.v1.views import ProfileCreateView

urlpatterns = [
    path("create/", ProfileCreateView.as_view(), name="profile_create"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
]
