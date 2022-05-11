from django.db import models


class ContactsGroup(models.Model):
    pass


class ContactType(models.Model):
    name = models.CharField(max_length=100)


class Contact(models.Model):
    contacts_group_id = models.ForeignKey(ContactsGroup, on_delete=models.CASCADE)
    type_ = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
