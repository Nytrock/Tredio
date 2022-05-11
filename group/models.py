from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from theatres.models import Event

User = get_user_model()


class Meetup(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start = models.DateTimeField()
    participants_limit = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    description = models.CharField(max_length=2500, null=True, blank=True)


class MeetupParticipant(models.Model):
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
