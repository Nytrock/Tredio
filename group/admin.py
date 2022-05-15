from django.contrib import admin

from group.models import Meetup, MeetupParticipant


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    list_display = ("id", "host", "event", "start")
    fields = ("host", "event", "start", "participants_limit", "description")


@admin.register(MeetupParticipant)
class MeetupParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "meetup", "user")
    fields = ("meetup", "user")
