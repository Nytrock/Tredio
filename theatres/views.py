from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from theatres.models import Event


class TheatresListView(TemplateView):
    template_name = "theatres/theatres_list.html"


class TheatresDetailView(TemplateView):
    template_name = "theatres/theatres_detail.html"


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


class EventCreateView(TemplateView):
    template_name = "theatres/events_create.html"

    def get_context_data(self, **kwargs):
        # Replace None with real form

        context = super().get_context_data(**kwargs)
        context["form"] = None
        return context
