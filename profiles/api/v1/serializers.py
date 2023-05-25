from django.contrib.auth.models import User
from rest_framework import serializers


def unique_email_validator(value):
    """
    Validate if email uniqueness is correctly validated during serialization.
    """

    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("Um usuário com este e-mail já existe.")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[unique_email_validator])

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
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
