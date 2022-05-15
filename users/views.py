from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from users.models import ActorProfile, UserProfile


class ActorProfileView(TemplateView):
    template_name = "users/actor_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(ActorProfile.actors.get_profile(kwargs["id"]))
        return context


class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def setup(self, request):
        super().setup(request)
        self.user_id: int = request.user.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(UserProfile.profiles.get_profile(self.user_id, private=True))
        return context


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(UserProfile.profiles.get_profile(kwargs["id"]))
        return context


class SignupView(TemplateView):
    template_name = "users/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserCreationForm()
        return context
