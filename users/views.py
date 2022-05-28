from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from core.models import Contact, ContactType
from group.models import Meetup, MeetupParticipant
from rating.models import Review
from theatres.models import TroupeMember
from users.forms import (
    ChangeContactsProfileForm,
    ChangeExtraProfileForm,
    ChangeMainProfileForm,
    CustomUserCreationForm,
)
from users.models import ActorProfile, Rank, UserProfile

User = get_user_model()


class ActorProfileView(TemplateView):
    template_name = "users/actor_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor_profile_id = kwargs["id"]
        troupes = list(TroupeMember.troupe_members.fetch_troupes_ids(actor_profile_id))

        context["profile"] = get_object_or_404(ActorProfile.common_profiles.get_profile(actor_profile_id))
        context["theatres"] = (
            ActorProfile.actor_profiles.get_theatres(actor_profile_id, troupes)
            .filter(is_published=True)
            .select_related("troupe", "location")
            .only("id", "image", "name", "description", "troupe", "location")
        )
        context["events"] = (
            ActorProfile.actor_profiles.get_events(actor_profile_id, troupes)
            .filter(is_published=True)
            .only("id", "image", "name", "description", "troupe")
        )
        context["profile_contacts"] = Contact.objects.filter(contacts_group=context["profile"].contacts)

        troupe_roles = dict()
        for (troupe, role) in TroupeMember.objects.filter(profile=actor_profile_id).values_list("troupe", "role").all():
            if troupe in troupe_roles:
                troupe_roles[troupe].append(role)
            elif role is not None:
                troupe_roles[troupe] = [role]

        for event in context["events"]:
            event.roles = troupe_roles.get(event.troupe.id, [])

        for theatre in context["theatres"]:
            theatre.roles = troupe_roles.get(theatre.troupe.id, [])

        return context


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        template = "users/profile.html"

        user = request.user
        profile = get_object_or_404(UserProfile.common_profiles.get_profile(user.id))
        user_profile = get_object_or_404(UserProfile.profiles.get_profile(user.id, private=True))

        form_main = ChangeMainProfileForm(
            request.POST or None,
            initial={
                User.email.field.name: user.email,
                User.username.field.name: user.username,
            },
        )
        form_extra = ChangeExtraProfileForm(request.POST or None)
        form_contacts = ChangeContactsProfileForm()

        context = {
            "main_form": form_main,
            "extra_form": form_extra,
            "contacts_form": form_contacts,
            "profile": profile,
            "user": user_profile,
            "meetups_host": Meetup.meetups.fetch_by_user(user),
            "meetups_participant": MeetupParticipant.meetup_participants.fetch_by_user(user),
            "reviews": Review.reviews.fetch_by_user(user),
            "contacts": ContactType.objects.all(),
        }
        context["next_rank"] = Rank.ranks.get_next_rank(user_profile.experience)

        if context["next_rank"] is not None:
            rank_experience_required = user_profile.rank.experience_required
            context["percent"] = int(
                (user_profile.experience - rank_experience_required)
                / (context["next_rank"].experience_required - rank_experience_required)
                * 100
            )
        context["profile_contacts"] = Contact.objects.filter(contacts_group=profile.contacts)

        return render(request, template, context)

    def post(self, request):
        user = request.user
        profile = user.user_profile

        form_main = ChangeMainProfileForm(request.POST)
        form_extra = ChangeExtraProfileForm(request.POST, request.FILES, instance=profile)
        form_contacts = ChangeContactsProfileForm(
            request.POST, fields=request.POST.get("field_count", 0), instance=profile.contacts
        )

        if form_main.is_valid():
            profile.first_name = form_main.cleaned_data["first_name"]
            profile.last_name = form_main.cleaned_data["last_name"]
            user.email = form_main.cleaned_data["email"]
            user.username = form_main.cleaned_data["username"]

            user.save()
            profile.save()

        if form_extra.is_valid():
            form_extra.save()

        if request.POST.get("contact-button") == "True":
            contacts = Contact.objects.filter(contacts_group=profile.contacts)
            for contact in contacts:
                value = request.POST.get(f"contact_{contact.id}")
                contact.value = value if value else None
                contact.save()

        if form_contacts.is_valid():
            form_contacts.save()

        return redirect("users:profile")


class UserDetailView(TemplateView):
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = kwargs["id"]

        user = get_object_or_404(User.objects, pk=profile_id)
        profile = get_object_or_404(UserProfile.common_profiles.get_profile(profile_id))

        context["profile"] = profile
        context["user"] = user
        context["meetups_participant"] = MeetupParticipant.meetup_participants.fetch_by_user(user)
        context["meetups_host"] = Meetup.meetups.fetch_by_user(user)
        context["profile_contacts"] = Contact.objects.filter(contacts_group=profile.contacts)

        return context

    def get(self, request, *args, **kwargs):
        if kwargs["id"] == request.user.id:
            return redirect("users:profile")
        return self.render_to_response(context=self.get_context_data(**kwargs))


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
