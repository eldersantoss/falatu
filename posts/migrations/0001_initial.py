# Generated by Django 4.2.1 on 2023-05-26 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criação"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="Atualização"),
                ),
                ("content", models.TextField(max_length=140, verbose_name="Conteúdo")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Postagem",
                "verbose_name_plural": "Postagens",
            },
        ),
    ]
