from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import Profile

from ..api.v1.serializers import PostSerializer
from ..models import Post


class PostSerializerTests(TestCase):
    def test_valid_deserialization(self):
        """
        Deserialization should be valid for provided valid data
        """

        data = {"content": "Test content"}
        serializer = PostSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["content"], data["content"])

    def test_valid_serialization(self):
        """
        Serialization should be valid for provided valid data
        """

        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        profile = Profile.objects.create(user=user)
        post = Post.objects.create(author=profile, content="Test content")
        serializer = PostSerializer(post)

        self.assertEqual(serializer.data["content"], post.content)

    def test_invalid_serialization_with_content_gt_max_length(self):
        """
        Serialization should NOT be valid because the content lenght
        """

        data = {"content": "Test content" * 100}
        serializer = PostSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("content", serializer.errors)
