from django import forms
from django.forms import CharField, Form, ModelForm, widgets

from core.models import Location
from core.validators import AddressValidator
from theatres.models import Event, Theatre
from users.models import ActorProfile


class TheatreForm(ModelForm):
    fias = forms.CharField(widget=forms.HiddenInput(attrs={"id": "location-fias"}))
    city = forms.CharField(widget=forms.HiddenInput(attrs={"id": "location-city"}))
    address = forms.CharField(
        label="Введите адрес театра",
        required=True,
        widget=widgets.TextInput(
            attrs={
                "id": "theatre-location",
                "class": "multi-form-input",
                "placeholder": "Адрес",
                "minlength": 1,
                "maxlength": Location._meta.get_field("query").max_length,
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        address_validator = AddressValidator(
            cleaned_data.get("address"), cleaned_data.get("city"), cleaned_data.get("fias")
        )
        address_validator()

    class Meta:
        model = Theatre
        fields = (Theatre.name.field.name, Theatre.description.field.name)

        labels = {
            Theatre.name.field.name: "Введите название театра",
            Theatre.description.field.name: "Введите описание театра",
        }

        widgets = {
            Theatre.name.field.name: widgets.TextInput(attrs={"class": "multi-form-input", "placeholder": "Название"}),
            Theatre.description.field.name: widgets.TextInput(
                attrs={"class": "multi-form-input", "placeholder": "Описание"}
            ),
        }

    field_order = [Theatre.name.field.name, "address", Theatre.description.field.name]


class SearchForm(Form):
    search = CharField(max_length=100, required=False)


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (Event.name.field.name, Event.theatre.field.name, Event.image.field.name, Event.description.field.name)

        labels = {
            Event.name.field.name: "Введите название постановки",
            Event.theatre.field.name: "Выберите театр",
            Event.image.field.name: "Выберите изображение",
            Event.description.field.name: "Введите описание постановки",
        }

        widgets = {
            Event.theatre.field.name: widgets.Select(attrs={"class": "multi-form-input"}),
            Event.name.field.name: widgets.TextInput(attrs={"class": "multi-form-input", "placeholder": "Название"}),
            Event.description.field.name: widgets.Textarea(attrs={"class": "multi-form-input"}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields[Event.image.field.name].required = False
        self.fields[Event.theatre.field.name].queryset = Theatre.objects.filter(is_published=True)


class ActorForm(ModelForm):
    class Meta:
        model = ActorProfile
        fields = (
            ActorProfile.first_name.field.name,
            ActorProfile.last_name.field.name,
            ActorProfile.birthday.field.name,
            ActorProfile.image.field.name,
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
            ActorProfile.image.field.name: "Загрузите фото актёра (необязательно)",
        }
