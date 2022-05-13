from django.forms import ModelForm, widgets

from theatres.models import Event, Location, Theatre


class TheatreForm(ModelForm):
    class Meta:
        model = Theatre
        fields = ("name", "location", "troupe")
        widgets = {
            "location": widgets.TextInput(
                attrs={"minlength": 1, "maxlength": Location._meta.get_field("query").max_length}
            )
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ("name", "theatre", "troupe")
