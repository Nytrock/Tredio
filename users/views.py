from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from core.models import Contact, ContactsGroup, ContactType
from group.models import Meetup, MeetupParticipant
from users.models import ActorProfile, UserProfile

from .forms import ChangeExtraProfileForm, ChangeMainProfileForm, CustomUserCreationForm

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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        template = "users/profile.html"
        self.user_id: int = request.user.id
        user = get_object_or_404(User.objects, pk=self.user_id)
        form_main = ChangeMainProfileForm(
            request.POST or None,
            initial={
                User.email.field.name: user.email,
                User.username.field.name: user.username,
            },
        )

        form_extra = ChangeExtraProfileForm(request.POST or None)

        context = {
            "main_form": form_main,
            "extra_form": form_extra,
            "profile": get_object_or_404(UserProfile.common_profiles.get_profile(self.user_id)),
            "user": get_object_or_404(UserProfile.profiles.get_profile(self.user_id)),
            "meetups_participant": MeetupParticipant.objects.filter(user_id=self.user_id).prefetch_related("event"),
            "meetups_host": Meetup.objects.filter(host_id=self.user_id).prefetch_related("event"),
            "reviews": UserProfile.profiles.get_reviews(self.user_id),
            "contacts": ContactType.objects.all(),
        }
        context["percent"] = int(context["profile"].experience / context["profile"].rank.experience_required * 100)
        context["profile_contacts"] = Contact.objects.filter(contacts_group_id=context["profile"].contacts)
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

        num = 1
        contact_data = {}
        while True:
            selection = request.POST.get("contact-label" + str(num))
            text = request.POST.get("contact-text" + str(num))
            if selection is not None and text is not None:
                contact_data[selection] = text
            else:
                break
            num += 1

        contacts = Contact.objects.filter(contacts_group_id=profile.contacts)
        for contact in contacts:
            contact.value = request.POST.get(contact.type.name)
            contact.save()

        for name in contact_data:
            Contact.objects.update_or_create(
                type_id=int(name),
                contacts_group_id_id=profile.contacts_id,
                defaults={"value": contact_data[name]},
            )

        return redirect("users:profile")


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["profile"] = get_object_or_404(UserProfile.common_profiles.get_profile(profile_id))
        context["user"] = get_object_or_404(UserProfile.profiles.get_profile(profile_id))
        context["meetups"] = UserProfile.profiles.get_meetups(profile_id)
        context["reviews"] = UserProfile.profiles.get_reviews(profile_id)

        return context


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = "users:login"

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
