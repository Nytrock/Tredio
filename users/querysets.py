from django.db import models

from theatres.models import Event, Theatre, TroupeMember


class ProfileQuerySet(models.QuerySet):
    def get_profile(self, id: int):
        return (
            self.filter(id=id)
            .select_related("contacts")
            .only("first_name", "last_name", "birthday", "description", "contacts")
        )


class ActorProfileQuerySet(models.QuerySet):
    def get_theatres(self, id: int, troupes_ids=None):
        if troupes_ids is None:
            troupes_ids = TroupeMember.troupe_members.fetch_troupes_ids(id)

        return Theatre.objects.filter(troupe__id__in=troupes_ids)

    def get_events(self, id: int, troupes_ids=None):
        if troupes_ids is None:
            troupes_ids = TroupeMember.troupe_members.fetch_troupes_ids(id)

        return Event.objects.filter(troupe__id__in=troupes_ids)


class RankQuerySet(models.QuerySet):
    def get_rank(self, experience: int):
        return self.filter(experience_required__lte=experience).order_by("-experience_required").first()

    def get_next_rank(self, experience: int):
        return self.filter(experience_required__gt=experience).order_by("experience_required").first()


class UserProfileQuerySet(models.QuerySet):
    def get_profile(self, id: int, private: bool = False):
        PUBLIC_FIELDS = ["rank"]
        PRIVATE_FIELDS = ["experience"]
        return (
            self.filter(id=id)
            .select_related("rank")
            .only(*(PUBLIC_FIELDS + PRIVATE_FIELDS if private else PUBLIC_FIELDS))
        )
