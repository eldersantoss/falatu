from django.db import models

from profiles.models import Profile


class TimeStampedModel(models.Model):
    created = models.DateTimeField("Criação", auto_now_add=True)
    modified = models.DateTimeField("Atualização", auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField("Conteúdo", max_length=140)
    image = models.ImageField(upload_to="post_images/", blank=True)

    class Meta:
        verbose_name = "postagem"
        verbose_name_plural = "postagens"
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"({self.created}) {self.author}: {self.content}"
