from django.contrib.auth.models import User
from django.db import DataError
from django.test import TestCase

from profiles.models import Profile

from ..models import Post


class PostModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_post_content_max_length(self):
        """
        The max length of post content should be equals to 140
        """

        post = Post.objects.create(author=self.profile, content="." * 140)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first(), post)
        with self.assertRaises(DataError):
            Post.objects.create(author=self.profile, content="." * 141)

    def test_verbose_name_and_verbose_name_plural(self):
        """
        verbose_name should be postagem and verbose_name_plural should be postagens
        """

        self.assertEqual(str(Post._meta.verbose_name), "postagem")
        self.assertEqual(str(Post._meta.verbose_name_plural), "postagens")

    def test_str_representation(self):
        """
        The model str should be in the format (<created_datetime>) <author_str_representation>: <content>
        """

        post = Post.objects.create(author=self.profile, content="Test post")
        self.assertEqual(str(post), f"({post.created}) {post.author}: {post.content}")
