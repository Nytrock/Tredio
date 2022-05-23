from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from core.models import Contact, ContactsGroup, ContactType
from group.models import Meetup, MeetupParticipant
from rating.models import Review
from theatres.models import TroupeMember
from users.models import ActorProfile, Rank, UserProfile

from .forms import ChangeExtraProfileForm, ChangeMainProfileForm, CustomUserCreationForm

User = get_user_model()


class ActorProfileView(TemplateView):
    template_name = "users/actor_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor_profile_id = kwargs["id"]
        troupes = list(TroupeMember.troupe_members.fetch_troupes_ids(actor_profile_id))

        context["profile"] = get_object_or_404(ActorProfile.common_profiles.get_profile(actor_profile_id))
        context["theatres"] = ActorProfile.actor_profiles.get_theatres(actor_profile_id, troupes).only(
            "id", "image", "name", "description", "troupe"
        )
        context["events"] = ActorProfile.actor_profiles.get_events(actor_profile_id, troupes).only(
            "id", "image", "name", "description", "troupe"
        )
        for event in context["events"]:
            troupe_member = TroupeMember.objects.filter(troupe_id=event.troupe.pk, profile_id=actor_profile_id).first()
            event.role = troupe_member.role
        for theatre in context["theatres"]:
            troupe_member = TroupeMember.objects.filter(
                troupe_id=theatre.troupe.pk, profile_id=actor_profile_id
            ).first()
            theatre.role = troupe_member.role
        context["profile_contacts"] = Contact.objects.filter(contacts_group_id=context["profile"].contacts)

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
            "meetups_host": Meetup.meetups.fetch_by_user(user),
            "meetups_participant": MeetupParticipant.meetups.fetch_by_user(user),
            "reviews": Review.reviews.fetch_by_user(user),
            "contacts": ContactType.objects.all(),
        }
        context["next_rank"] = Rank.ranks.get_next_rank(context["profile"].experience)
        if context["next_rank"] is not None:
            context["percent"] = int(context["profile"].experience / context["next_rank"].experience_required * 100)
        context["profile_contacts"] = Contact.objects.filter(contacts_group_id=context["profile"].contacts)
        return render(request, template, context)

    def post(self, request):
        user = get_object_or_404(User.objects, pk=request.user.id)
        profile = user.user_profile

        form_main = ChangeMainProfileForm(request.POST)
        form_extra = ChangeExtraProfileForm(request.POST, request.FILES, instance=profile)

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
            form_extra.save()

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

        if request.POST.get("contact-button") == "True":
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
        profile_id = kwargs["id"]

        context["profile"] = get_object_or_404(UserProfile.common_profiles.get_profile(profile_id))
        user = get_object_or_404(User.objects, pk=context["profile"].user_id)
        context["user"] = get_object_or_404(User.objects, pk=user.id)
        context["meetups_participant"] = MeetupParticipant.meetups.fetch_by_user(user)
        context["meetups_host"] = Meetup.meetups.fetch_by_user(user)
        context["profile_contacts"] = Contact.objects.filter(contacts_group_id=context["profile"].contacts)

        return context


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = "users:login"

    def form_valid(self, form):
        User = get_user_model()
        first_name = form.cleaned_data[UserProfile.first_name.field.name]
        last_name = form.cleaned_data[UserProfile.last_name.field.name]
        contacts = ContactsGroup.objects.create()
        user = User.objects.create_user(
            username=form.cleaned_data[User.username.field.name],
            password=form.cleaned_data["password2"],
            email=form.cleaned_data[User.email.field.name],
        )
        UserProfile.objects.filter(user=user).update(
            first_name=first_name,
            last_name=last_name,
            birthday=form.cleaned_data["birthday"],
            description=form.cleaned_data["description"],
            experience=0,
            rank=Rank.objects.filter(experience_required=0).first(),
            contacts_id=contacts.id,
        )
        return redirect("users:login")
