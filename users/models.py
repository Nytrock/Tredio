from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import ContactsGroup, ImageBaseModel, PublishedBaseModel
from theatres.models import Event, Theatre, TroupeMember
from users.querysets import (
    ActorProfileQuerySet,
    ProfileQuerySet,
    RankQuerySet,
    UserProfileQuerySet,
)

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField("Название", max_length=100)

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class UserAchievement(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, verbose_name="Достижение", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Достижение пользователя"
        verbose_name_plural = "Достижения пользователей"


class CommonProfile(ImageBaseModel):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    birthday = models.DateField("Дата рождения", null=True, blank=True)
    description = models.CharField("О себе", max_length=2500, null=True, blank=True)
    contacts = models.ForeignKey(
        ContactsGroup, verbose_name="Контакты", on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = models.Manager()
    common_profiles = ProfileQuerySet.as_manager()

    class Meta:
        abstract = True


class ActorProfile(CommonProfile, PublishedBaseModel):
    objects = models.Manager()
    actor_profiles = ActorProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "Профиль актера"
        verbose_name_plural = "Профили актеров"

    def __str__(self):
        return self.first_name + " " + self.last_name


class ModerationActorProfile(ActorProfile):
    class Meta:
        verbose_name = "Профиль актера на модерации"
        verbose_name_plural = "Профили актеров на модерации"
        proxy = True


class Rank(models.Model):
    name = models.CharField("Название", max_length=100)
    color = ColorField(null=True, blank=True)
    experience_required = models.IntegerField("Необходимый опыт")

    objects = models.Manager()
    ranks = RankQuerySet.as_manager()

    class Meta:
        verbose_name = "Ранг"
        verbose_name_plural = "Ранги"


class UserProfile(CommonProfile):
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_profile"
    )
    rank = models.ForeignKey(Rank, verbose_name="Ранг", on_delete=models.RESTRICT, null=True, blank=True)
    experience = models.IntegerField("Опыт", default=0)

    objects = models.Manager()
    profiles = UserProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


def update_rank(sender, instance, **kwargs):
    new_rank = Rank.ranks.get_rank(instance.experience)
    if instance.rank != new_rank:
        instance.rank = new_rank


def add_experience(id, xp):
    profile = UserProfile.objects.filter(user_id=id).first()
    profile.experience += xp
    profile.save()
