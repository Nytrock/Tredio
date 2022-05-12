from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class ProfileChangeView(TemplateView):
    template_name = "users/profile_change.html"


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"


class ActorDetailView(TemplateView):
    template_name = "users/profile_actor.html"


class SignupView(TemplateView):
    template_name = "users/signup.html"
