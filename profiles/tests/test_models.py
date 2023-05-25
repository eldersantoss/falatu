from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user)
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.user, self.user)

    def test_profile_str_representation(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), self.user.get_full_name())

    def test_profile_verbose_name_plural(self):
        self.assertEqual(str(Profile._meta.verbose_name_plural), "Perfis")
