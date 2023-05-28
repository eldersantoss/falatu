from typing import Self

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
    )

    def __str__(self) -> str:
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def get_absolute_url(self):
        return reverse("profile_detail", args=[self.user.username])

    def follow(self, profile: Self):
        self.following.add(profile)
        profile.followers.add(self)

    def unfollow(self, profile: Self):
        self.following.remove(profile)
        profile.followers.remove(self)

    def get_following(self):
        return self.following.all()

    def get_followers(self):
        return self.followers.all()

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()
