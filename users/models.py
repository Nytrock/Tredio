from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import ContactsGroup, ImageBaseModel, PublishedBaseModel
from theatres.models import Event, Theatre, TroupeMember

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


class ProfileQuerySet(models.QuerySet):
    def get_profile(self, id: int):
        return (
            self.filter(id=id)
            .select_related("contacts")
            .only("first_name", "last_name", "birthday", "description", "contacts")
        )


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


class ActorProfileQuerySet(models.QuerySet):
    def get_theatres(self, id: int, troupes_ids=None):
        if troupes_ids is None:
            troupes_ids = TroupeMember.troupe_members.fetch_troupes_ids(id)

        return Theatre.objects.filter(troupe__id__in=troupes_ids)

    def get_events(self, id: int, troupes_ids=None):
        if troupes_ids is None:
            troupes_ids = TroupeMember.troupe_members.fetch_troupes_ids(id)

        return Event.objects.filter(troupe__id__in=troupes_ids)


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


class RankQuerySet(models.QuerySet):
    def get_rank(self, experience: int):
        return self.filter(experience_required__lte=experience).order_by("-experience_required").first()

    def get_next_rank(self, experience: int):
        return self.filter(experience_required__gt=experience).order_by("experience_required").first()


class Rank(models.Model):
    name = models.CharField("Название", max_length=100)
    color = ColorField(null=True, blank=True)
    experience_required = models.IntegerField("Необходимый опыт")

    objects = models.Manager()
    ranks = RankQuerySet.as_manager()

    class Meta:
        verbose_name = "Ранг"
        verbose_name_plural = "Ранги"


class UserProfileQuerySet(models.QuerySet):
    def get_profile(self, id: int, private: bool = False):
        PUBLIC_FIELDS = ["rank__name"]
        PRIVATE_FIELDS = ["experience"]
        return (
            self.filter(id=id)
            .prefetch_related("contacts")
            .only(*(PUBLIC_FIELDS + PRIVATE_FIELDS if private else PUBLIC_FIELDS))
        )


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


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.user_profile.save()


def update_rank(sender, instance, **kwargs):
    new_rank = Rank.ranks.get_rank(instance.experience)
    if instance.rank != new_rank:
        instance.rank = new_rank


def add_experience(id, xp):
    profile = UserProfile.objects.filter(user_id=id).first()
    profile.experience += xp
    profile.save()
