from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from core.models import ContactsGroup

from .forms import ChangeExtraProfileForm, ChangeMainProfileForm, CustomUserCreationForm
from .models import UserProfile

User = get_user_model()


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        template = "users/profile.html"
        user = get_object_or_404(User.objects, pk=request.user.id)
        form_main = ChangeMainProfileForm(
            request.POST or None,
            initial={
                User.first_name.field.name: user.first_name,
                User.last_name.field.name: user.last_name,
                User.email.field.name: user.email,
                "username": user.username,
            },
        )

        profile = UserProfile.objects.filter(user=user.id).first()
        form_extra = ChangeExtraProfileForm(
            request.POST or None,
            initial={
                UserProfile.birthday.field.name: profile.birthday,
                UserProfile.description.field.name: profile.description,
            },
        )

        context = {
            "main_form": form_main,
            "extra_form": form_extra,
        }
        return render(request, template, context)

    def post(self, request):
        form_main = ChangeMainProfileForm(request.POST)
        form_extra = ChangeExtraProfileForm(request.POST)

        user = get_object_or_404(User.objects, pk=request.user.id)
        profile = UserProfile.objects.filter(user=user.id).first()

        if form_main.is_valid():
            first_name = form_main.cleaned_data["first_name"]
            last_name = form_main.cleaned_data["last_name"]
            user.first_name = first_name
            profile.first_name = first_name
            user.last_name = last_name
            profile.last_name = last_name
            user.email = form_main.cleaned_data["email"]
            user.username = form_main.cleaned_data["username"]

            user.save()
            profile.save()

        if form_extra.is_valid():
            if form_extra.cleaned_data[UserProfile.description.field.name]:
                profile.description = form_extra.cleaned_data[UserProfile.description.field.name]
            if form_extra.cleaned_data[UserProfile.birthday.field.name]:
                profile.birthday = form_extra.cleaned_data[UserProfile.birthday.field.name]
            profile.save()

        return redirect("users:profile")


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"


class ActorDetailView(TemplateView):
    template_name = "users/profile_actor.html"


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = "users:login"

    def form_valid(self, form):
        User = get_user_model()
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        contacts = ContactsGroup.objects.create()
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password2"],
            email=form.cleaned_data["email"],
            first_name=first_name,
            last_name=last_name,
        )
        UserProfile.objects.create(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            birthday=form.cleaned_data["birthday"],
            description=form.cleaned_data["description"],
            experience=0,
            rank_id=1,
            contacts_id=contacts.id,
        )
        return redirect("users:login")
