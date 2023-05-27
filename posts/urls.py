from django.urls import path

from posts.api.v1 import views

urlpatterns = [
    path(
        "",
        views.PostListView.as_view(),
        name="post_list",
    ),
    path(
        "followed/",
        views.FollowedPostListView.as_view(),
        name="followed_post_list",
    ),
    path(
        "create/",
        views.PostCreateView.as_view(),
        name="create_post",
    ),
]
