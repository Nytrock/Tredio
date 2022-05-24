from django.contrib import admin

from core.models import Contact, ContactsGroup, ContactType


@admin.register(ContactsGroup)
class ContactsGroupAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    fields = ("name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "contacts_group", "type", "value")
    fields = ("contacts_group", "type", "value")
