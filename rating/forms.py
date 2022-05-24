from django.forms import ModelForm, widgets

from rating.models import Review


class RatingForm(ModelForm):
    class Meta:
        model = Review
        fields = (Review.category.field.name, Review.content.field.name)

        widgets = {
            Review.content.field.name: widgets.Textarea(attrs={"class": "form-control", "placeholder": "Содержание"}),
            Review.category.field.name: widgets.Select(attrs={"class": "form-control"}),
        }
