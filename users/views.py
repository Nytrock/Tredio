from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from users.models import ActorProfile


class ActorProfileView(TemplateView):
    template_name = "users/actor_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(ActorProfile.actors.get_profile(kwargs["id"]))
        return context


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"


class SignupView(TemplateView):
    template_name = "users/signup.html"
