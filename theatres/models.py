from django.db import models

from core.models import ContactsGroup
from rating.models import ReviewGroup
from users.models import ActorProfile


class Troupe(models.Model):
    class Meta:
        verbose_name = "Труппа"
        verbose_name_plural = "Труппы"


class TroupeMember(models.Model):
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.CASCADE)
    profile = models.ForeignKey(ActorProfile, verbose_name="Профиль", on_delete=models.CASCADE)
    role = models.CharField(verbose_name="Роль", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Участник труппы"
        verbose_name_plural = "Участники трупп"


class City(models.Model):
    name = models.CharField("Название", max_length=100)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Location(models.Model):
    """
    Информация о местоположении.
    Полем `query` следует пользоваться лишь в тех случаях, когда идентификатор ФИАС устарел.
    """

    #: Адрес одной строкой
    query = models.CharField("Адрес", max_length=250)

    #: Город
    city = models.ForeignKey(City, verbose_name="Город", on_delete=models.CASCADE)

    #: Уникальный идентификатор ФИАС
    fias = models.CharField("ФИАС", max_length=50)

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"


class Theatre(models.Model):
    name = models.CharField("Название", max_length=150)
    location = models.ForeignKey(Location, verbose_name="Местоположение", on_delete=models.CASCADE)
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(ReviewGroup, verbose_name="Отзывы", on_delete=models.SET_NULL, null=True, blank=True)
    contacts = models.ForeignKey(
        ContactsGroup, verbose_name="Контакты", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Театр"
        verbose_name_plural = "Театры"


class Event(models.Model):
    name = models.CharField("Название", max_length=150)
    theatre = models.ForeignKey(Theatre, verbose_name="Театр", on_delete=models.CASCADE)
    troupe = models.ForeignKey(Troupe, verbose_name="Труппа", on_delete=models.SET_NULL, null=True, blank=True)
    reviews = models.ForeignKey(ReviewGroup, verbose_name="Отзывы", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
