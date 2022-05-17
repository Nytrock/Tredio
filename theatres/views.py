from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from core.models import ContactsGroup
from rating.models import ReviewGroup
from theatres.forms import EventForm, TheatreForm
from theatres.models import Event, Troupe, TroupeMember
from users.models import ActorProfile


class TheatresListView(TemplateView):
    template_name = "theatres/theatres_list.html"


class TheatresDetailView(TemplateView):
    template_name = "theatres/theatres_detail.html"


class TheatresCreateView(FormView):
    template_name = "theatres/theatres_create.html"
    form_class = TheatreForm
    success_url = "theatres:theatres_list"

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        pass


class EventListView(TemplateView):
    template_name = "theatres/events_list.html"


class EventDetailView(TemplateView):
    template_name = "theatres/events_detail.html"


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
            image=form.cleaned_data["image"],
            name=form.cleaned_data["name"],
            reviews_id=reviews.id,
            theatre_id=form.cleaned_data["theatre"].id,
            troupe_id=troupe.id,
        )
        return redirect("theatres:events_list")
