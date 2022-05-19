from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from users.models import ActorProfile, UserProfile


class ActorProfileView(TemplateView):
    template_name = "users/actor_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor_profile_id = kwargs["id"]
        troupes = list(ActorProfile.actor_profiles.get_troupe_ids(actor_profile_id))

        context["profile"] = get_object_or_404(ActorProfile.common_profiles.get_profile(actor_profile_id))
        context["theatres"] = ActorProfile.actor_profiles.get_theatres(actor_profile_id, troupes).only(
            "id", "image", "name", "description"
        )
        context["events"] = ActorProfile.actor_profiles.get_events(actor_profile_id, troupes).only(
            "id", "image", "name", "description"
        )

        return context


class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def setup(self, request):
        super().setup(request)
        self.user_id: int = request.user.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = get_object_or_404(UserProfile.common_profiles.get_profile(self.user_id))
        context["user"] = get_object_or_404(UserProfile.profiles.get_profile(self.user_id))
        context["meetups"] = UserProfile.profiles.get_meetups(self.user_id)
        context["reviews"] = UserProfile.profiles.get_reviews(self.user_id)

        return context


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = kwargs["id"]

        context["profile"] = get_object_or_404(UserProfile.common_profiles.get_profile(profile_id))
        context["user"] = get_object_or_404(UserProfile.profiles.get_profile(profile_id))
        context["meetups"] = UserProfile.profiles.get_meetups(profile_id)
        context["reviews"] = UserProfile.profiles.get_reviews(profile_id)

        return context


class SignupView(TemplateView):
    template_name = "users/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserCreationForm()
        return context
