from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


def modify_fields(**kwargs):
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls

    return wrap


class ContactsGroup(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = "Группа контактов"
        verbose_name_plural = "Группы контактов"


class ContactType(models.Model):
    name = models.CharField("Название", max_length=100)

    objects = models.Manager()

    class Meta:
        verbose_name = "Тип контакта"
        verbose_name_plural = "Типы контактов"

    def __str__(self):
        return self.name


class Contact(models.Model):
    contacts_group = models.ForeignKey(
        ContactsGroup, related_name="contacts", verbose_name="Группа контактов", on_delete=models.CASCADE
    )
    type = models.ForeignKey(ContactType, verbose_name="Тип контакта", on_delete=models.CASCADE)
    value = models.CharField("Значение", max_length=100)

    objects = models.Manager()

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class City(models.Model):
    name = models.CharField("Название", max_length=100)

    objects = models.Manager()

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


class ImageBaseModel(models.Model):
    image = models.ImageField("Изображение", upload_to="uploads/", null=True, blank=True)

    def get_image_x1280(self):
        return get_thumbnail(self.image, "1280", quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.image, "400x300", crop="center", quality=51)

    def get_image_1400x800(self):
        return get_thumbnail(self.image, "1400x800", crop="center", quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(f"<img src='{self.image.url}' width='50'/>")
        return "Нет изображения"

    image_tmb.allow_tags = True
    image_tmb.short_description = "Изображение"

    class Meta:
        abstract = True


@modify_fields(image={"verbose_name": "Изображение галереи"})
class GalleryBaseModel(ImageBaseModel):
    class Meta:
        abstract = True
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галерей"


class PublishedBaseModel(models.Model):
    is_published = models.BooleanField("Опубликовано", default=False)

    class Meta:
        abstract = True
