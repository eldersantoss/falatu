from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserCreateViewTests(APITestCase):
    def test_create_user(self):
        """
        Should create a new user through UserCreateView.
        """

        url = reverse("user_create")
        data = {
            "username": "test",
            "email": "test@email.com",
            "password": "test123",
            "first_name": "Test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.first_name, data["first_name"])

    def test_create_user_missing_required_field(self):
        """
        Should not create the user with missing required fields through UserCreateView.
        """

        url = reverse("user_create")
        data = {
            "username": "test",
            "password": "test123",
            "first_name": "Test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_invalid_data(self):
        """
        Should not create user with invalid data through UserCreateView.
        """

        url = reverse("user_create")
        data = {
            "username": "test",
            "email": "invalid_email",
            "password": "test123",
            "first_name": "Test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
