from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import ContactsGroup
from theatres.models import Event, Theatre

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


class CommonProfile(models.Model):
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
    def get_troupes_ids(self, id: int):
        return self.filter(id=id).prefetch_related("troupe_members__troupe__id").only()

    def get_theatres(self, id: int, troupes_ids=None):
        if troupes == None:
            troupes = get_troupes_ids(id)

        return Theatre.objects.filter(troupe__id__in=troupes)

    def get_events(self, id: int, troupes_ids=None):
        if troupes == None:
            troupes = get_troupes_ids()

        return Event.objects.filter(troupe__id__in=troupes)


class ActorProfile(CommonProfile):
    objects = models.Manager()
    actor_profiles = ActorProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "Профиль актера"
        verbose_name_plural = "Профили актеров"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Rank(models.Model):
    name = models.CharField("Название", max_length=100)
    experience_required = models.CharField("Необходимый опыт", max_length=100)

    class Meta:
        verbose_name = "Ранг"
        verbose_name_plural = "Ранги"


class UserProfileQuerySet(models.QuerySet):
    def get_profile(self, id: int, private: bool = False):
        PUBLIC_FIELDS = ["rank__name"]
        PRIVATE_FIELDS = ["experience"]
        return self.filter(id=id).only(*(PUBLIC_FIELDS + PRIVATE_FIELDS if private else PUBLIC_FIELDS))


class UserProfile(CommonProfile):
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_profile"
    )
    rank = models.ForeignKey(Rank, verbose_name="Ранг", on_delete=models.RESTRICT)
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
