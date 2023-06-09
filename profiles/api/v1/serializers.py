from django.contrib.auth.models import User
from rest_framework import serializers

from ...models import Profile


def unique_email_validator(value):
    """
    Validate if email uniqueness is correctly validated during serialization.
    """

    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Um usuário com este e-mail já existe.")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[unique_email_validator],
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    following = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "user",
            "following",
            "followers",
        )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password")
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        profile = Profile.objects.create(user=user)
        return profile

    def get_following(self, obj):
        return obj.get_following_count()

    def get_followers(self, obj):
        return obj.get_followers_count()
