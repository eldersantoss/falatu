from rest_framework import serializers

from profiles.api.v1.serializers import ProfileSerializer

from ...models import Post


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "content", "image", "created")
        extra_kwargs = {
            "created": {"read_only": True},
        }
