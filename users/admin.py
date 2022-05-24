from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import (
    Achievement,
    ActorProfile,
    ModerationActorProfile,
    Rank,
    UserAchievement,
    UserProfile,
)

User = get_user_model()


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    fields = ("name",)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "achievement")
    fields = ("user", "achievement")


@admin.register(ActorProfile)
class ActorProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birthday", "contacts", "is_published")
    fields = ("first_name", "last_name", "birthday", "contacts", "description", "is_published")


@admin.register(ModerationActorProfile)
class ModerationActorProfileAdmin(ActorProfileAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_published=False)


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "experience_required", "color")
    fields = ("name", "experience_required", "color")


class UserProfileInlined(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInlined,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
