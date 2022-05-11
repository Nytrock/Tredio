from django.contrib.auth import get_user_model
from django.db import models

from core.models import ContactsGroup

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField(max_length=100)


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)


class CommonProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=2500, null=True, unique=True)
    contacts = models.ForeignKey(ContactsGroup, on_delete=models.SET_NULL, null=True, unique=True)

    class Meta:
        abstract = True


class ActorProfile(CommonProfile):
    pass


class Profile(CommonProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Rank(models.Model):
    name = models.CharField(max_length=100)
    experience_required = models.CharField(max_length=100)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL)
    experience = models.IntegerField()
