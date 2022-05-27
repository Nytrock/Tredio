from django.db import models

from core.models import (
    ContactsGroup,
    GalleryBaseModel,
    ImageBaseModel,
    Location,
    PublishedBaseModel,
)
from rating.models import ReviewGroup
from theatres.querysets import EventQuerySet, TheatreQuerySet, TroupeMemberQuerySet


class Troupe(models.Model):
    class Meta:
        verbose_name = "Труппа"
        verbose_name_plural = "Труппы"


class TroupeMember(models.Model):
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", related_name="members", on_delete=models.CASCADE)
    profile = models.ForeignKey(
        to="users.ActorProfile", verbose_name="Профиль", on_delete=models.CASCADE, related_name="troupe_members"
    )
    role = models.CharField(verbose_name="Роль", max_length=100, null=True, blank=True)

    objects = models.Manager()
    troupe_members = TroupeMemberQuerySet.as_manager()

    class Meta:
        verbose_name = "Участник труппы"
        verbose_name_plural = "Участники трупп"


class Theatre(PublishedBaseModel, ImageBaseModel):
    name = models.CharField("Название", max_length=150)
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name="Местоположение", on_delete=models.CASCADE)
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(ReviewGroup, verbose_name="Отзывы", on_delete=models.SET_NULL, null=True, blank=True)
    contacts = models.ForeignKey(
        ContactsGroup, verbose_name="Контакты", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = models.Manager()
    theatres = TheatreQuerySet.as_manager()

    class Meta:
        verbose_name = "Театр"
        verbose_name_plural = "Театры"

    def __str__(self):
        return self.name


class ModerationTheatre(Theatre):
    class Meta:
        verbose_name = "Театр на модерации"
        verbose_name_plural = "Театры на модерации"
        proxy = True


class TheatreImage(GalleryBaseModel):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="gallery_images")


class Event(PublishedBaseModel, ImageBaseModel):
    name = models.CharField("Название", max_length=150)
    description = models.CharField("Описание", max_length=2500, null=True, blank=True)
    theatre = models.ForeignKey(Theatre, verbose_name="Театр", on_delete=models.CASCADE, related_name="events")
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(ReviewGroup, verbose_name="Отзывы", on_delete=models.SET_NULL, null=True, blank=True)

    objects = models.Manager()
    events = EventQuerySet.as_manager()

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return self.name


class ModerationEvent(Event):
    class Meta:
        verbose_name = "Событие на модерации"
        verbose_name_plural = "События на модерации"
        proxy = True


class EventImage(GalleryBaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="gallery_images")
