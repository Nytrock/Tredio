from django.forms import ModelForm
from groups.models import Meetup


class MeetupForm(ModelForm):
    class Meta:
        model = Meetup
        fields = ("event", "start", "description", "participants_limit")
        widgets = {}
