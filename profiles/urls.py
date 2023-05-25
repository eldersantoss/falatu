from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api.v1.views import UserCreateView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
]
