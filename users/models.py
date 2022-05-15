from django.contrib.auth import get_user_model
from django.db import models

from core.models import ContactsGroup

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


class CommonProfile(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    birthday = models.DateField("Дата рождения", null=True, blank=True)
    description = models.CharField("О себе", max_length=2500, null=True, blank=True)
    contacts = models.ForeignKey(
        ContactsGroup, verbose_name="Контакты", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        abstract = True


class ActorProfileQuerySet(models.QuerySet):
    def get_profile(self, id: int):
        return (
            self.filter(id=id)
            .prefetch_related("contacts__contacts")
            .only("first_name", "last_name", "birthday", "description")
        )


class ActorProfile(CommonProfile):
    objects = models.Manager()
    actors = ActorProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "Профиль актера"
        verbose_name_plural = "Профили актеров"


class Rank(models.Model):
    name = models.CharField("Название", max_length=100)
    experience_required = models.CharField("Необходимый опыт", max_length=100)

    class Meta:
        verbose_name = "Ранг"
        verbose_name_plural = "Ранги"


class UserProfile(CommonProfile):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, verbose_name="Ранг", on_delete=models.RESTRICT)
    experience = models.IntegerField("Опыт", default=0)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
