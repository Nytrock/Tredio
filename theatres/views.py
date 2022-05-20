from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView

from core.models import Contact, ContactsGroup, ContactType
from rating.models import ReviewGroup
from theatres.forms import ActorForm, EventForm, TheatreForm
from theatres.models import City, Event, Theatre, Troupe, TroupeMember
from users.models import ActorProfile


class TheatresListView(TemplateView):
    template_name = "theatres/theatres_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theatres"] = Theatre.theatres.theatres_list()
        context["cities"] = City.objects.all()
        return context


class TheatresDetailView(TemplateView):
    template_name = "theatres/theatres_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theatre"] = get_object_or_404(Theatre.theatres.theatre_details(kwargs["id"]))
        return context


class TheatresCreateView(TemplateView):
    template_name = "theatres/theatres_create.html"

    def get_context_data(self, **kwargs):
        # Replace None with real form

        context = super().get_context_data(**kwargs)
        context["form"] = None
        return context


class EventListView(TemplateView):
    template_name = "theatres/events_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.events.events_list()
        context["cities"] = City.objects.all()
        return context


class EventDetailView(TemplateView):
    template_name = "theatres/events_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = get_object_or_404(Event.events.event_details(kwargs["id"]))
        return context


class ActorListView(TemplateView):
    template_name = "theatres/actors_list.html"


class ActorCreateView(FormView):
    template_name = "theatres/actors_create.html"
    form_class = ActorForm
    success_url = "theatres:events_list"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["contacts"] = ContactType.objects.all()
        context["id"] = kwargs.get("id")
        return self.render_to_response(context)

    def form_valid(self, form):
        num = 1
        contact_data = {}
        while True:
            try:
                actor = form.data["contact_type" + str(num)]
            except:
                break
            try:
                role = form.data["value" + str(num)]
            except:
                break
            contact_data[actor] = role
            num += 1
        group = ContactsGroup.objects.create()
        for name in contact_data:
            contact_type = ContactType.objects.filter(name=name).first()
            Contact.objects.create(
                value=contact_data[name],
                type_id=contact_type.id,
                contacts_group_id_id=group.id,
            )
        ActorProfile.objects.create(
            first_name=form.cleaned_data[ActorProfile.first_name.field.name],
            last_name=form.cleaned_data[ActorProfile.last_name.field.name],
            description=form.cleaned_data[ActorProfile.description.field.name],
            birthday=form.cleaned_data[ActorProfile.birthday.field.name],
            contacts_id=group.id,
        )
        return redirect("homepage:home")


class EventCreateView(FormView):
    template_name = "theatres/events_create.html"
    form_class = EventForm
    success_url = "theatres:events_list"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["actors"] = ActorProfile.objects.all()
        return self.render_to_response(context)

    def form_valid(self, form):
        num = 1
        troupe_data = {}
        while True:
            try:
                actor = form.data["actor_change" + str(num)]
            except:
                break
            try:
                role = form.data["role" + str(num)]
            except:
                role = ""
            troupe_data[actor] = role
            num += 1
        reviews = ReviewGroup.objects.create()
        troupe = Troupe.objects.create()
        for name in troupe_data:
            actor = ActorProfile.objects.filter(first_name=name.split()[0], last_name=name.split()[1]).first()
            TroupeMember.objects.create(profile_id=actor.id, troupe_id=troupe.id, role=troupe_data[name])
        Event.objects.create(
            image=form.cleaned_data[Event.image.field.name],
            name=form.cleaned_data[Event.name.field.name],
            description=form.cleaned_data[Event.description.field.name],
            reviews_id=reviews.id,
            theatre_id=form.cleaned_data[Event.theatre.field.name].id,
            troupe_id=troupe.id,
        )
        return redirect("theatres:events_list")
