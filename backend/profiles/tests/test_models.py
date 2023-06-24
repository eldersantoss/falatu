from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from ..models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test123",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_str_representation(self):
        """
        The profile str representation should be equals to user full name
        """
        self.assertEqual(str(self.profile), self.user.get_full_name())

    def test_profile_verbose_name_plural(self):
        """
        The profile verbose name plural should be equals to perfis
        """
        self.assertEqual(str(Profile._meta.verbose_name_plural), "Perfis")

    def test_get_absolute_url(self):
        """
        The absolute url should to have /api/v1/profiles/<username>/ format
        """

        url = self.profile.get_absolute_url()
        self.assertEqual(url, f"/api/v1/profiles/{self.profile.user}/")

    def test_follow_profile(self):
        """
        another_profile should be in self.profile.following and self.profile should be in another_profile.followers
        """

        another_profile = mommy.make(Profile)
        self.profile.follow(another_profile)

        self.assertIn(another_profile, self.profile.following.all())
        self.assertIn(self.profile, another_profile.followers.all())

    def test_unfollow_profile(self):
        """
        another_profile should not be in self.profile.following and self.profile should not be in another_profile.followers
        """

        another_profile = mommy.make(Profile)
        self.profile.follow(another_profile)

        self.assertIn(another_profile, self.profile.following.all())
        self.assertIn(self.profile, another_profile.followers.all())

        self.profile.unfollow(another_profile)

        self.assertNotIn(another_profile, self.profile.following.all())
        self.assertNotIn(self.profile, another_profile.followers.all())

    def test_get_following_and_get_following_count(self):
        """
        get_following should be equals to profile.following.all() and get_following_count should be equals to profile.following.count()
        """

        followed_profile1, followed_profile2, followed_profile3 = mommy.make(
            Profile, _quantity=3
        )
        self.profile.follow(followed_profile1)
        self.profile.follow(followed_profile2)
        self.profile.follow(followed_profile3)

        self.assertCountEqual(
            self.profile.get_following(), self.profile.following.all()
        )
        self.assertEqual(self.profile.get_following_count(), 3)

    def test_get_followers_and_get_followers_count(self):
        """
        get_followers should be equals to profile.followers.all() and get_followers_count should be equals to profile.followers.count()
        """

        following_profile1, following_profile2, following_profile3 = mommy.make(
            Profile, _quantity=3
        )
        following_profile1.follow(self.profile)
        following_profile2.follow(self.profile)
        following_profile3.follow(self.profile)

        self.assertCountEqual(
            self.profile.get_followers(), self.profile.followers.all()
        )
        self.assertEqual(self.profile.get_followers_count(), 3)
