from django.test import TestCase

from ..api.v1.serializers import PostSerializer


class PostSerializerTests(TestCase):
    def test_valid_serialization(self):
        """
        Serialization should be considered valid for provided valid data
        """

        data = {"content": "Test content"}
        serializer = PostSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["content"], data["content"])

    def test_invalid_serialization_with_content_gt_max_length(self):
        """
        Serialization should NOT be valid because the content lenght
        """

        data = {"content": "Test content" * 100}
        serializer = PostSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("content", serializer.errors)
