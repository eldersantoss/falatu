from django.contrib.auth.models import User
from django.urls import reverse
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
