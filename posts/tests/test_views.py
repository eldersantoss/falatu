from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from profiles.models import Profile


class PostCreateViewTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_post_creation(self):
        """
        A post should be created with the logged user as author
        """

        self.client.force_authenticate(user=self.user)
        url = reverse("create_post")
        data = {"content": "Test post"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().author, self.profile)

    def test_post_creation_with_unauthenticated_user(self):
        """
        The action should be unauthorized and the post should not be created
        """

        url = reverse("create_post")
        data = {"content": "Test post"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_creation_with_unauthenticated_user(self):
        """
        The action should be unauthorized and the post should not be created
        """

        url = reverse("create_post")
        data = {"content": "Test post"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_creation_with_invalid_content(self):
        """
        The post should not be created because content data is not valid
        """

        self.client.force_authenticate(user=self.user)
        url = reverse("create_post")
        data = {"content": ""}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)


class PostListViewTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_number_of_posts_per_page(self):
        """
        The max number of posts per page should be 10, the surplus should be in next page
        """

        mommy.make(Post, _quantity=15)

        self.client.force_authenticate(user=self.user)
        url = reverse("post_list")
        response = self.client.get(url)

        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

        url = response.data["next"]
        response = self.client.get(url)
        self.assertEqual(len(response.data["results"]), 5)

    def test_post_list_exclude_logged_user_posts(self):
        """
        The legged user posts should not be in post list
        """

        mommy.make(Post, content="Post from another user")
        Post.objects.create(author=self.profile, content="Logged user post")

        self.client.force_authenticate(user=self.user)
        url = reverse("post_list")
        response = self.client.get(url)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertContains(response, "Post from another user")
        self.assertNotContains(response, "Logged user post")


class FollowingPostListViewTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_only_followed_posts_are_returned(self):
        """
        Only posts of followed profiles should be returned
        """

        followed_profile = mommy.make(Profile)
        not_followed_profile = mommy.make(Profile)
        self.profile.follow(followed_profile)

        mommy.make(
            Post,
            author=followed_profile,
            content="Followed profile post",
        )
        mommy.make(
            Post,
            author=not_followed_profile,
            content="Not followed profile post",
        )

        self.client.force_authenticate(user=self.user)
        url = reverse("followed_post_list")
        response = self.client.get(url)

        self.assertContains(
            response=response,
            text="Followed profile post",
            count=1,
            status_code=status.HTTP_200_OK,
        )
        self.assertNotContains(
            response=response,
            text="Not followed profile post",
        )
