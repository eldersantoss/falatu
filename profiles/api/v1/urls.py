from django.urls import path

from profiles.api.v1.views import UserCreateView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user_create")
]
