from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from theatres.models import Event


class TheatresListView(TemplateView):
    template_name = "theatres/theatres_list.html"


class TheatresDetailView(TemplateView):
    template_name = "theatres/theatres_detail.html"


class TheatresCreateView(TemplateView):
    template_name = "theatres/theatres_create.html"


class EventListView(TemplateView):
    template_name = "theatres/events_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.events.events_list()
        return context


class EventDetailView(TemplateView):
    template_name = "theatres/events_detail.html"


class EventCreateView(TemplateView):
    template_name = "theatres/events_create.html"
