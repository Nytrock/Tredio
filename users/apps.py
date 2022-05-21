from django.apps import AppConfig
from fieldsignals import pre_save_changed


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from .models import UserProfile, update_rank

        pre_save_changed.connect(receiver=update_rank, sender=UserProfile, fields=["experience"])
