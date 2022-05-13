from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, widgets

from .models import UserProfile

User = get_user_model()


class CustomUserCreationForm(ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput(attrs={"placeholder": "Подтвеждение пароля"})
    )
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    birthday = forms.DateField(label="День рождения", required=False)
    description = forms.CharField(widget=widgets.Textarea, label="О себе", required=False)

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            "username": widgets.TextInput(
                attrs={"minlength": 1, "maxlength": User._meta.get_field("username").max_length}
            )
        }

        labels = {"username": "Никнейм"}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].initial = UserProfile._meta.get_field("first_name")
        self.fields["last_name"].initial = UserProfile._meta.get_field("last_name")
        self.fields["birthday"].initial = UserProfile._meta.get_field("birthday")
        self.fields["description"].initial = UserProfile._meta.get_field("description")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
