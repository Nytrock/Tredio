from django.contrib import admin

from theatres.models import City, Event, Location, Theatre, Troupe, TroupeMember


@admin.register(Troupe)
class TroupeAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(TroupeMember)
class TroupeMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "troupe", "profile", "role")
    fields = ("troupe", "profile", "role")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "city", "fias")
    fields = ("query", "city", "fias")


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "troupe", "reviews", "contacts")
    fields = ("name", "location", "troupe", "reviews", "contacts")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "theatre", "troupe", "reviews")
    fields = ("name", "theatre", "troupe", "reviews")
