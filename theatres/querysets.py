from django.db import models
from django.db.models import Prefetch, Q

from rating.models import ReviewRating


class TroupeMemberQuerySet(models.QuerySet):
    def fetch_troupes_ids(self, profile: int):
        return self.filter(profile__id=profile).values_list("troupe", flat=True)

    def fetch_troupes_roles(self, profile: int):
        return self.filter(profile__id=profile).values_list("role", flat=True)

    def fetch(self, troupe_id: int):
        return self.filter(troupe__id=troupe_id)


class TheatreQuerySet(models.QuerySet):
    def theatres_list(self):
        return (
            self.only("id", "image", "name", "description", "location__query")
            .order_by("name")
            .filter(is_published=True)
        )

    def theatre_search(self, search_query: str):
        return self.theatres_list().filter(name__icontains=search_query)

    def theatre_details(self, id: int):
        from theatres.models import Event

        return (
            self.filter(id=id)
            .prefetch_related(
                "gallery_images",
                "reviews__reviews",
                Prefetch("events", queryset=Event.objects.filter(is_published=True)),
                "events__meetups",
                "events__meetups__host",
            )
            .only("name", "description")
            .annotate(
                reviews_count=models.Count("reviews__reviews", distinct=True),
                reviews_average_score=models.Avg("reviews__reviews__star"),
                events_count=models.Count("events", filter=Q(events__is_published=True), distinct=True),
            )
        )

    def theatre_ratings(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related(
                "reviews__reviews",
                "reviews__reviews__user__user_profile",
                Prefetch("reviews__reviews__ratings", to_attr="like", queryset=ReviewRating.objects.filter(star=True)),
                Prefetch(
                    "reviews__reviews__ratings", to_attr="dislike", queryset=ReviewRating.objects.filter(star=False)
                ),
            )
            .only("id", "name", "image", "location__query", "description")
        )


class EventQuerySet(models.QuerySet):
    def events_list(self):
        return (
            self.only("id", "image", "name", "description", "theatre__id", "theatre__name", "theatre__location__query")
            .order_by("name")
            .filter(is_published=True)
        )

    def event_search(self, search_query: str):
        return self.events_list().filter(name__icontains=search_query)

    def event_details(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related("troupe__members", "reviews__reviews")
            .only("id", "image", "name", "description", "theatre__id", "theatre__name", "theatre__location__query")
            .annotate(
                reviews_count=models.Count("reviews__reviews"),
                reviews_average_score=models.Avg("reviews__reviews__star"),
            )
        )

    def event_ratings(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related(
                "reviews__reviews",
                Prefetch("reviews__reviews__ratings", to_attr="like", queryset=ReviewRating.objects.filter(star=True)),
                Prefetch(
                    "reviews__reviews__ratings", to_attr="dislike", queryset=ReviewRating.objects.filter(star=False)
                ),
            )
            .only(
                "id",
                "name",
                "image",
                "description",
                "theatre__id",
                "theatre__name",
                "theatre__image",
                "theatre__location__query",
            )
        )
