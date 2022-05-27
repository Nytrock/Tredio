from django.contrib.auth import get_user_model
from django.db import models

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


class MeetupParticipantQuerySet(models.QuerySet):
    def fetch_by_user(self, user: User):
        return self.filter(user=user)

    def fetch_by_meetup(self, meetup):
        return self.filter(meetup=meetup)
