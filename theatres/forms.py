from django.forms import ModelForm, widgets

from theatres.models import Event, Location, Theatre
from users.models import ActorProfile


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


class ActorForm(ModelForm):
    class Meta:
        model = ActorProfile
        fields = (
            ActorProfile.first_name.field.name,
            ActorProfile.last_name.field.name,
            ActorProfile.birthday.field.name,
            ActorProfile.description.field.name,
        )

        widgets = {
            ActorProfile.first_name.field.name: widgets.TextInput(
                attrs={"class": "multi-form-input", "placeholder": "Имя"}
            ),
            ActorProfile.last_name.field.name: widgets.TextInput(
                attrs={"class": "multi-form-input", "placeholder": "Фамилия"}
            ),
            ActorProfile.description.field.name: widgets.Textarea(attrs={"class": "multi-form-input"}),
            ActorProfile.birthday.field.name: widgets.DateTimeInput(
                attrs={"class": "multi-form-input", "placeholder": "День рождения", "type": "date"}
            ),
        }

        labels = {
            ActorProfile.first_name.field.name: "Введите имя",
            ActorProfile.last_name.field.name: "Введите фамилию",
            ActorProfile.description.field.name: "Введите описание актёра",
            ActorProfile.birthday.field.name: "Введите дату рождения (необязательно)",
        }
