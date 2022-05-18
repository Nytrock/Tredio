from django.forms import ModelForm, widgets

from .models import Meetup


class MeetupForm(ModelForm):
    class Meta:
        model = Meetup
        fields = (
            Meetup.event.field.name,
            Meetup.start.field.name,
            Meetup.description.field.name,
            Meetup.participants_limit.field.name,
        )
        widgets = {
            Meetup.event.field.name: widgets.Select(attrs={"class": "multi-form-input"}),
            Meetup.start.field.name: widgets.DateTimeInput(attrs={"class": "multi-form-input", "type": "date"}),
            Meetup.description.field.name: widgets.Textarea(attrs={"class": "multi-form-input"}),
            Meetup.participants_limit.field.name: widgets.NumberInput(attrs={"class": "multi-form-input"}),
        }

        labels = {
            Meetup.event.field.name: "Постановка, ради которой создаётся группа",
            Meetup.start.field.name: "Дата встречи",
            Meetup.description.field.name: "Описание группы",
            Meetup.participants_limit.field.name: "Лимит участников группы",
        }
