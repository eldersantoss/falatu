# Generated by Django 4.2.1 on 2023-05-26 02:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"verbose_name": "postagem", "verbose_name_plural": "postagens"},
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.CharField(max_length=140, verbose_name="Conteúdo"),
        ),
    ]
