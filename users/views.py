from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import ContactsGroup
from .forms import ChangeExtraProfileForm, ChangeMainProfileForm, CustomUserCreationForm
from users.models import ActorProfile, UserProfile

User = get_user_model()


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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def setup(self, request):
        super().setup(request)
        self.user_id: int = request.user.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
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

        context["profile"] = get_object_or_404(UserProfile.common_profiles.get_profile(self.user_id))
        context["user"] = get_object_or_404(UserProfile.profiles.get_profile(self.user_id))
        context["meetups"] = UserProfile.profiles.get_meetups(self.user_id)
        context["reviews"] = UserProfile.profiles.get_reviews(self.user_id)
        context["main_form"] = form_main
        context["extra_form"] = form_extra

        return context
      
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
        context["form"] = CustomUserCreationForm()
        return context
      
    def form_valid(self, form):
        User = get_user_model()
        first_name = form.cleaned_data[User.first_name.field.name]
        last_name = form.cleaned_data[User.last_name.field.name]
        contacts = ContactsGroup.objects.create()
        user = User.objects.create_user(
            username=form.cleaned_data[User.username.field.name],
            password=form.cleaned_data["password2"],
            email=form.cleaned_data[User.email.field.name],
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
