from django.forms import ModelForm, widgets

from theatres.models import Event, Location, Theatre


class TheatreForm(ModelForm):
    class Meta:
        model = Theatre
        fields = (Theatre.name.field.name, Theatre.location.field.name, Theatre.troupe.field.name)
        widgets = {
            Theatre.location.field.name: widgets.TextInput(
                attrs={"minlength": 1, "maxlength": Location._meta.get_field("query").max_length}
            )
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (Event.name.field.name, Event.theatre.field.name, Event.image.field.name)

        labels = {
            Event.name.field.name: "Введите название постановки",
            Event.theatre.field.name: "Выберите театр",
            Event.image.field.name: "Выберите изображение",
        }

        widgets = {
            Event.theatre.field.name: widgets.Select(attrs={"class": "multi-form-input"}),
            Event.name.field.name: widgets.TextInput(attrs={"class": "multi-form-input", "placeholder": "Название"}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields[Event.image.field.name].required = False
