# Generated by Django 4.0.4 on 2022-05-15 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rating", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="review_group_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="rating.reviewgroup",
                verbose_name="Группа отзывов",
            ),
        ),
    ]