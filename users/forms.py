from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, widgets

from users.models import UserProfile

User = get_user_model()


class CustomUserCreationForm(ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Пароль",
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Подтвеждение пароля",
                "class": "form-control",
            }
        ),
    )
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Фамилия"})
    )
    birthday = forms.DateField(
        label="День рождения",
        required=False,
        widget=forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "День Рождения", "type": "date"}),
    )
    description = forms.CharField(
        label="О себе",
        required=False,
        widget=widgets.Textarea(attrs={"class": "form-control", "placeholder": "О себе"}),
    )

    email = forms.EmailField(required=True, label="Почта")

    class Meta:
        model = User
        fields = (User.username.field.name, User.email.field.name)
        widgets = {
            "username": widgets.TextInput(
                attrs={
                    "minlength": 1,
                    "maxlength": User._meta.get_field("username").max_length,
                    "class": "form-control",
                    "placeholder": "Имя",
                }
            ),
            "email": widgets.TextInput(
                attrs={
                    "minlength": 1,
                    "maxlength": User._meta.get_field("email").max_length,
                    "class": "form-control",
                    "placeholder": "Почта",
                }
            ),
        }

        labels = {
            "username": "Логин",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


class ChangeMainProfileForm(ModelForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={
                "minlength": 1,
                "maxlength": User._meta.get_field("username").max_length,
            }
        ),
    )

    class Meta:
        model = User
        fields = (User.email.field.name, User.first_name.field.name, User.last_name.field.name)
        labels = {
            User.email.field.name: "Почта",
            User.first_name.field.name: "Имя",
            User.last_name.field.name: "Фамилия",
        }


class ChangeExtraProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = (UserProfile.birthday.field.name, UserProfile.description.field.name)
        labels = {
            UserProfile.birthday.field.name: "День рождения",
            UserProfile.description.field.name: "Описание",
        }
