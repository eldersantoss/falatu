from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from ..api.v1.serializers import (
    ProfileSerializer,
    UserSerializer,
    unique_email_validator,
)
from ..models import Profile


class UserSerializerTests(TestCase):
    def test_unique_email_validator_raises_error(self):
        """
        unique_email_validator should raise a ValidationError for an existing email.
        """

        existing_email = "existing@email.com"
        User.objects.create_user(
            username="test",
            email=existing_email,
            password="test123",
        )

        with self.assertRaises(serializers.ValidationError):
            unique_email_validator(existing_email)

    def test_unique_email_validator_no_error(self):
        """
        unique_email_validator should NOT raise a ValidationError for a unique email.
        """

        new_email = "new@email.com"

        try:
            unique_email_validator(new_email)
        except serializers.ValidationError:
            self.fail("unique_email_validator raised ValidationError incorrectly")

    def test_user_serialization_omit_sensible_data(self):
        """
        Serialization should omit user sensible data like id, email and password
        """

        user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

        serializer = UserSerializer(user)

        self.assertEqual(serializer.data["username"], user.username)
        self.assertEqual(serializer.data["first_name"], user.first_name)
        self.assertEqual(serializer.data["last_name"], user.last_name)
        self.assertNotIn("id", serializer.data)
        self.assertNotIn("password", serializer.data)
        self.assertNotIn("email", serializer.data)

    def test_valid_user_deserialization(self):
        """
        Deserialization should be considered valid for provided valid data.
        """

        valid_data = {
            "username": "test",
            "email": "test@email.com",
            "password": "test123",
            "first_name": "Test",
            "last_name": "User",
        }

        serializer = UserSerializer(data=valid_data)

        self.assertTrue(serializer.is_valid())

    def test_email_uniqueness_validation(self):
        """
        Email uniqueness should be correctly validated during serialization.
        """

        existing_email = "existing@email.com"
        User.objects.create_user(
            username="test",
            email=existing_email,
            password="test123",
        )

        data = {
            "username": "test",
            "email": existing_email,
            "password": "test123",
            "first_name": "John",
        }

        serializer = UserSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_create_user(self):
        """
        Should create new User instance and set password.
        """

        data = {
            "username": "test",
            "email": "test@email.com",
            "password": "test123",
            "first_name": "Test",
        }

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.first_name, "Test")
        self.assertTrue(user.check_password("test123"))


class ProfileSerializerTests(TestCase):
    def test_profile_serialization_result(self):
        """
        Serialization should omit profile sensible data like id
        """

        user = User.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        profile = Profile.objects.create(user=user)

        serializer = ProfileSerializer(profile)

        self.assertNotIn("id", serializer.data)
        self.assertIn("user", serializer.data)

        self.assertEqual(profile.user.username, serializer.data["user"]["username"])
        self.assertEqual(profile.user.first_name, serializer.data["user"]["first_name"])
        self.assertEqual(profile.user.last_name, serializer.data["user"]["last_name"])
        self.assertEqual(profile.get_following_count(), serializer.data["following"])
        self.assertEqual(profile.get_followers_count(), serializer.data["followers"])

    def test_valid_profile_deserialization(self):
        """
        Deserialization should be considered valid for provided valid data
        """

        valid_data = {
            "user": {
                "username": "test",
                "email": "test@email.com",
                "password": "test123",
                "first_name": "Test",
            }
        }

        serializer = ProfileSerializer(data=valid_data)

        self.assertTrue(serializer.is_valid())

    def test_following_and_followers_count(self):
        ...
