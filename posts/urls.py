from django.urls import path

from posts.api.v1 import views

urlpatterns = [
    path("create/", views.PostCreateView.as_view(), name="create_post"),
]
