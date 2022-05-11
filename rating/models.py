from django.contrib.auth import get_user_model
from django.db import models

from core.validators import RangeValidator

User = get_user_model()


class ReviewGroup(models.Model):
    pass

    class Meta:
        verbose_name = "Группа отзывов"
        verbose_name_plural = "Группы отзывов"


class ReviewCategory(models.Model):
    name = models.CharField("Название", max_length=100)

    class Meta:
        verbose_name = "Категория отзыва"
        verbose_name_plural = "Категории отзывов"


class Review(models.Model):
    review_group_id = models.ForeignKey(ReviewGroup, verbose_name="Группа отзывов", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    category = models.ForeignKey(ReviewCategory, verbose_name="Категория", on_delete=models.CASCADE)
    star = models.IntegerField("Оценка", validators=[RangeValidator(1, 5)])
    content = models.CharField("Содержание", max_length=2500, null=True, blank=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class ReviewRating(models.Model):
    review = models.ForeignKey(Review, verbose_name="Отзыв", related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    star = models.BooleanField("Оценка")

    class Meta:
        verbose_name = "Оценка отзыва"
        verbose_name_plural = "Оценки отзывов"
