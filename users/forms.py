from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm, widgets

from core.models import Contact, ContactsGroup, ContactType
from theatres.forms import MultipleKeyValueForm
from users.models import Rank, UserProfile

User = get_user_model()

FIRST_NAME_FIELD = forms.CharField(
    label="Имя",
    widget=widgets.Textarea(
        attrs={
            "maxlength": UserProfile._meta.get_field("first_name").max_length,
            "class": "form-control",
            "placeholder": "Имя",
        }
    ),
)

LAST_NAME_FIELD = forms.CharField(
    label="Фамилия",
    widget=widgets.Textarea(
        attrs={
            "maxlength": UserProfile._meta.get_field("last_name").max_length,
            "class": "form-control",
            "placeholder": "Фамилия",
        }
    ),
)


class CustomUserCreationForm(ModelForm):
    first_name = FIRST_NAME_FIELD

    last_name = LAST_NAME_FIELD

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

    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )
        widgets = {
            User.username.field.name: widgets.TextInput(
                attrs={
                    "minlength": 1,
                    "maxlength": User._meta.get_field("username").max_length,
                    "class": "form-control",
                    "placeholder": "Логин",
                }
            ),
            User.email.field.name: widgets.TextInput(
                attrs={
                    "minlength": 1,
                    "maxlength": User._meta.get_field("email").max_length,
                    "class": "form-control",
                    "placeholder": "Почта",
                }
            ),
        }

        labels = {
            User.username.field.name: "Логин",
            User.email.field.name: "Почта",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields[User.email.field.name].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def save(self):
        first_name = self.cleaned_data[UserProfile.first_name.field.name]
        last_name = self.cleaned_data[UserProfile.last_name.field.name]
        contacts = ContactsGroup.objects.create()
        user = User.objects.create_user(
            username=self.cleaned_data[User.username.field.name],
            password=self.cleaned_data["password2"],
            email=self.cleaned_data[User.email.field.name],
        )
        UserProfile.objects.create(
            id=user.id,
            user=user,
            first_name=first_name,
            last_name=last_name,
            birthday=self.cleaned_data["birthday"],
            description=self.cleaned_data["description"],
            experience=0,
            rank=Rank.objects.filter(experience_required=0).first(),
            contacts_id=contacts.id,
        )


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

    first_name = FIRST_NAME_FIELD

    last_name = LAST_NAME_FIELD

    class Meta:
        model = User
        fields = (User.email.field.name,)
        labels = {
            User.email.field.name: "Почта",
        }


class ChangeContactsProfileForm(MultipleKeyValueForm):
    def __init__(self, *args, **kwargs):
        super().__init__(
            forms.ModelChoiceField(queryset=ContactType.objects.all()),
            forms.CharField(max_length=Contact._meta.get_field("value").max_length),
            *args,
            **kwargs,
        )

    def save(self, commit=True):
        contacts_data = [(self.cleaned_data[key], self.cleaned_data[value]) for (key, value) in self.multiple_fields()]

        contacts = self.instance
        contacts.save()
        contacts_objects = []

        for contact_type, contact_value in contacts_data:
            contacts_objects.append(Contact(contacts_group=contacts, type=contact_type, value=contact_value))
        Contact.objects.bulk_create(contacts_objects)

        if commit:
            contacts.save()
        return contacts

    class Meta:
        model = ContactsGroup
        fields = tuple()


class ChangeExtraProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = (UserProfile.birthday.field.name, UserProfile.description.field.name, UserProfile.image.field.name)
        labels = {
            UserProfile.birthday.field.name: "День рождения",
            UserProfile.description.field.name: "Описание",
        }
