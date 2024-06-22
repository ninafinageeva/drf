# Generated by Django 5.0.6 on 2024-06-22 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
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
                    "name",
                    models.CharField(
                        help_text="введите название курса",
                        max_length=100,
                        verbose_name="название курса",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="введите описание курса",
                        null=True,
                        verbose_name="описание курса",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="выберите изображение",
                        null=True,
                        upload_to="materials/course",
                        verbose_name="изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
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
                    "name",
                    models.CharField(
                        help_text="введите название",
                        max_length=100,
                        verbose_name="название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="введите описание",
                        null=True,
                        verbose_name="описание урока",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="выберите изображение",
                        null=True,
                        upload_to="materials/lesson",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        help_text="добавьте ссылку",
                        null=True,
                        verbose_name="ссылка",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        help_text="выберите курс",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course",
                        to="materials.course",
                        verbose_name="курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "урок",
                "verbose_name_plural": "уроки",
            },
        ),
    ]
