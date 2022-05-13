from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from .forms import CustomUserCreationForm
from .models import UserProfile


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class ProfileChangeView(TemplateView):
    template_name = "users/profile_change.html"


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
        user = User.objects.create_user(username=form.cleaned_data["username"], password=form.cleaned_data["password2"])
        UserProfile.objects.create(
            user_id=user.id,
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            birthday=form.cleaned_data["birthday"],
            description=form.cleaned_data["description"],
            experience=0,
            rank_id=1,
        )
        return redirect("users:login")
