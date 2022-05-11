from django.contrib.auth import get_user_model
from django.db import models

from core.validators import RangeValidator

User = get_user_model()


class ReviewGroup(models.Model):
    pass


class ReviewCategory(models.Model):
    name = models.CharField(max_length=100)


class Review(models.Model):
    review_group_id = models.ForeignKey(ReviewGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ReviewCategory, on_delete=models.CASCADE)
    star = models.IntegerField(validators=[RangeValidator(1, 5)])
    content = models.CharField(max_length=2500, null=True, blank=True)


class ReviewRating(models.Model):
    review = models.ForeignKey(Review, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.BooleanField()
