from django.db import models


class ContactsGroup(models.Model):
    class Meta:
        verbose_name = "Группа контактов"
        verbose_name_plural = "Группы контактов"


class ContactType(models.Model):
    name = models.CharField("Название", max_length=100)

    class Meta:
        verbose_name = "Тип контакта"
        verbose_name_plural = "Типы контактов"


class Contact(models.Model):
    contacts_group_id = models.ForeignKey(ContactsGroup, verbose_name="Группа контактов", on_delete=models.CASCADE)
    type = models.ForeignKey(ContactType, verbose_name="Тип контакта", on_delete=models.CASCADE)
    value = models.CharField("Значение", max_length=100)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
