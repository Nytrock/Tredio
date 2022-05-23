from django.forms import ModelForm, widgets

from theatres.models import Event

from .models import Meetup


class MeetupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetupForm, self).__init__(*args, **kwargs)
        self.fields[Meetup.event.field.name].queryset = Event.objects.filter(is_published=True)

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
