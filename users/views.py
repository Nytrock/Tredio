from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = 'users/profile.html'


class UserDetailView(TemplateView):
    template_name = 'users/user_detail.html'


class SignupView(TemplateView):
    template_name = 'users/signup.html'
