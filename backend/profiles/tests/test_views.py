from django.contrib.auth.models import User
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Profile


class ProfileCreateViewTests(APITestCase):
    def test_create_user(self):
        """
        Should create a new user and your profile
        """

        url = reverse("profile_create")
        data = {
            "user": {
                "username": "test",
                "email": "test@email.com",
                "password": "test123",
                "first_name": "Test",
            }
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        user = User.objects.get()
        profile = Profile.objects.get()

        self.assertEqual(user.username, data["user"]["username"])
        self.assertEqual(user.email, data["user"]["email"])
        self.assertTrue(user.check_password(data["user"]["password"]))
        self.assertEqual(user.first_name, data["user"]["first_name"])
        self.assertEqual(user.profile, profile)

    def test_create_user_missing_required_field(self):
        """
        Should not create the user because required fields are missing
        """

        url = reverse("profile_create")
        data = {
            "user": {
                "username": "test",
                "password": "test123",
                "first_name": "Test",
            }
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_invalid_data(self):
        """
        Should not create user because data is invalid
        """

        url = reverse("profile_create")
        data = {
            "username": "test",
            "email": "invalid_email",
            "password": "test123",
            "first_name": "Test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class ProfileRetrieveViewTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_detail(self):
        """
        Should return profile data including number of following and followers
        """

        url = reverse("profile_detail", args=[self.profile.user.username])
        response = self.client.get(url)

        self.assertEqual(
            response.data["user"]["username"],
            self.profile.user.username,
        )
        self.assertEqual(
            response.data["user"]["first_name"],
            self.profile.user.first_name,
        )
        self.assertEqual(
            response.data["user"]["last_name"],
            self.profile.user.last_name,
        )
        self.assertEqual(
            response.data["following"],
            self.profile.get_following_count(),
        )
        self.assertEqual(
            response.data["followers"],
            self.profile.get_followers_count(),
        )


class ProfileFollowersViewTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_follow_and_unfollow_actions(self):
        """
        Should follow/unfollow profile and get follower count of logged in profile and followers count of followed/unfollowed profile updated
        """

        followed_profile = mommy.make(Profile, user__username="followeduser")
        response = self.client.post(
            reverse(
                "profile_followers",
                kwargs={"username": followed_profile.user.username},
            )
        )

        self.assertContains(
            response=response,
            text="logged_in_following",
            status_code=status.HTTP_200_OK,
        )

        self.assertEqual(self.profile.get_following_count(), 1)
        self.assertEqual(followed_profile.get_followers_count(), 1)
        self.assertEqual(
            self.profile.get_following_count(),
            response.data["logged_in_following"],
        )
        self.assertEqual(
            followed_profile.get_followers_count(),
            response.data["target_followers"],
        )

        response = self.client.post(followed_profile.get_absolute_url() + "followers/")

        self.assertEqual(self.profile.get_following_count(), 0)
        self.assertEqual(followed_profile.get_followers_count(), 0)
        self.assertEqual(
            self.profile.get_following_count(),
            response.data["logged_in_following"],
        )
        self.assertEqual(
            followed_profile.get_followers_count(),
            response.data["target_followers"],
        )
