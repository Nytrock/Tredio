from django import forms
from django.forms import ModelForm, widgets

from rating.models import Review


class RatingForm(ModelForm):
    star = forms.IntegerField(
        min_value=1, max_value=5, widget=widgets.NumberInput(attrs={"class": "form-control", "placeholder": "Тескт"})
    )

    class Meta:
        model = Review
        fields = (Review.content.field.name, Review.category.field.name)

        widgets = {
            Review.content.field.name: widgets.Textarea(attrs={"class": "form-control", "placeholder": "Тескт"}),
            Review.category.field.name: widgets.Select(attrs={"class": "form-control"}),
        }
