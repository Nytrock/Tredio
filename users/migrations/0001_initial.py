# Generated by Django 4.0.4 on 2022-05-12 04:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Достижение",
                "verbose_name_plural": "Достижения",
            },
        ),
        migrations.CreateModel(
            name="Rank",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("experience_required", models.CharField(max_length=100, verbose_name="Необходимый опыт")),
            ],
            options={
                "verbose_name": "Ранг",
                "verbose_name_plural": "Ранги",
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                ("birthday", models.DateField(blank=True, null=True, verbose_name="Дата рождения")),
                ("description", models.CharField(blank=True, max_length=2500, null=True, verbose_name="О себе")),
                ("experience", models.IntegerField(default=0, verbose_name="Опыт")),
                (
                    "contacts",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.contactsgroup",
                        verbose_name="Контакты",
                    ),
                ),
                (
                    "rank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="users.rank", verbose_name="Ранг"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль пользователя",
                "verbose_name_plural": "Профили пользователей",
            },
        ),
        migrations.CreateModel(
            name="UserAchievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "achievement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.achievement", verbose_name="Достижение"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Достижение пользователя",
                "verbose_name_plural": "Достижения пользователей",
            },
        ),
        migrations.CreateModel(
            name="ActorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                ("birthday", models.DateField(blank=True, null=True, verbose_name="Дата рождения")),
                ("description", models.CharField(blank=True, max_length=2500, null=True, verbose_name="О себе")),
                (
                    "contacts",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.contactsgroup",
                        verbose_name="Контакты",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль актера",
                "verbose_name_plural": "Профили актеров",
            },
        ),
    ]