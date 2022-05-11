from django.db import models


class Troupe(models.Model):
    pass


class TroupeMember(models.Model):
    troupe_id = models.ForeignKey(Troupe, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)


class City(models.Model):
    name = models.CharField(max_length=100)


class Location(models.Model):
    """
    Информация о местоположении.
    Полем `query` следует пользоваться лишь в тех случаях, когда идентификатор ФИАС устарел.
    """

    #: Адрес одной строкой
    query = models.CharField(max_length=250)

    #: Город
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    #: Уникальный идентификатор ФИАС
    fias = models.CharField(max_length=50)


class Theatre(models.Model):
    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL)
    troupe = models.ForeignKey(Troupe, on_delete=models.SET_NULL)
    reviews = models.ForeignKey(ReviewGroup, on_delete=models.SET_NULL)
