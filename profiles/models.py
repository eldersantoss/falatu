from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
