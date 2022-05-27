from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ReviewQuerySet(models.QuerySet):
    def fetch_by_user(self, user: User):
        return self.filter(user=user)
