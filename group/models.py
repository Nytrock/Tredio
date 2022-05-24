from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from theatres.models import Event

User = get_user_model()


class MeetupQuerySet(models.QuerySet):
    def _meetups(self):
        return self.only(
            "event__id",
            "event__image",
            "host__username",
            "host__user_profile__first_name",
            "host__user_profile__last_name",
            "start",
            "participants_limit",
            "description",
        )

    def meetup_list(self):
        return self._meetups().annotate(participants_count=models.Count("participants"))

    def meetup_search(self, search_query: str):
        return (
            self._meetups()
            .filter(event__name__icontains=search_query)
            .annotate(participants_count=models.Count("participants"))
        )

    def meetup_details(self, meetup_id: int):
        return (
            self.filter(id=meetup_id)
            .prefetch_related("event__troupe", "participants__user", "participants__user__user_profile")
            .only(
                "event__theatre__id",
                "event__theatre__name",
                "event__theatre__location__query",
                "event__image",
                "host__username",
                "host__user_profile__first_name",
                "host__user_profile__last_name",
                "start",
                "participants_limit",
                "description",
            )
            .annotate(participants_count=models.Count("participants"))
        )

    def fetch_by_user(self, user: User):
        return self.filter(host=user)


class Meetup(models.Model):
    host = models.ForeignKey(User, verbose_name="Организатор", on_delete=models.CASCADE, related_name="meetups")
    event = models.ForeignKey(Event, verbose_name="Событие", on_delete=models.CASCADE, related_name="meetups")
    start = models.DateTimeField(verbose_name="Время встречи")
    participants_limit = models.IntegerField(
        "Максимальное кол-во участников", validators=[MinValueValidator(1)], null=True, blank=True
    )
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)

    objects = models.Manager()
    meetups = MeetupQuerySet.as_manager()

    def is_participant(self, user: User):
        return (
            user == self.host or MeetupParticipant.meetup_participants.fetch_by_meetup(self).filter(user=user).exists()
        )

    class Meta:
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"


class MeetupParticipantQuerySet(models.QuerySet):
    def fetch_by_user(self, user: User):
        return self.filter(user=user)

    def fetch_by_meetup(self, meetup: Meetup):
        return self.filter(meetup=meetup)


class MeetupParticipant(models.Model):
    meetup = models.ForeignKey(Meetup, verbose_name="Встреча", related_name="participants", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Участник", on_delete=models.CASCADE)

    objects = models.Manager()
    meetup_participants = MeetupParticipantQuerySet.as_manager()

    class Meta:
        verbose_name = "Участник встречи"
        verbose_name_plural = "Участники встреч"
