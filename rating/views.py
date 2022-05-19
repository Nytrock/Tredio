from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from theatres.models import Event, Theatre


class RatingTheatreView(TemplateView):
    template_name = "rating/rating_theatre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = get_object_or_404(Theatre.theatres.theatre_ratings(kwargs["id"]))
        return context


class RatingEventView(TemplateView):
    template_name = "rating/rating_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = get_object_or_404(Event.events.event_ratings(kwargs["id"]))
        return context


class RatingCreateView(TemplateView):
    template_name = "rating/rating_create.html"

    def get_context_data(self, **kwargs):
        # Replace None with real form

        context = super().get_context_data(**kwargs)
        context["form"] = None
        return context
