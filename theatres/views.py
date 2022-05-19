from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView

from core.models import Contact, ContactsGroup, ContactType
from rating.models import ReviewGroup
from theatres.forms import ActorForm, EventForm, TheatreForm
from theatres.models import Event, Troupe, TroupeMember
from users.models import ActorProfile
from theatres.models import Event, Theatre


class TheatresListView(TemplateView):
    template_name = "theatres/theatres_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theatres"] = Theatre.theatres.theatres_list()
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

class EventCreateView(TemplateView):
    template_name = "theatres/events_create.html"

    def get_context_data(self, **kwargs):
        form = self.get_form(form_class)
        context = super().get_context_data(**kwargs)
        context["form"] = form
        context["actors"] = ActorProfile.objects.all()
        return context
      
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
