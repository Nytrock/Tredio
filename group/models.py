from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from theatres.models import Event

User = get_user_model()


class Meetup(models.Model):
    host = models.ForeignKey(User, verbose_name="Организатор", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name="Событие", on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name="Время встречи")
    participants_limit = models.IntegerField(
        "Максимальное кол-во участников", validators=[MinValueValidator(1)], null=True, blank=True
    )
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)

    class Meta:
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"


class MeetupParticipant(models.Model):
    meetup = models.ForeignKey(Meetup, verbose_name="Встреча", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Участник", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Участник встречи"
        verbose_name_plural = "Участники встреч"
