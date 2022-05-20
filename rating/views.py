from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from rating.forms import RatingForm
from rating.models import Review
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
        form = RatingForm()

        context = super().get_context_data(**kwargs)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = RatingForm(request.POST)
        if kwargs.get("type") == "theatre":
            theatre = get_object_or_404(Theatre.objects, pk=kwargs.get("id"))
            Review.objects.create(
                star=form.data["star"],
                content=form.data["content"],
                category_id=form.data["category"],
                review_group_id_id=theatre.reviews.id,
                user_id=request.user.id,
            )
        else:
            event = get_object_or_404(Event.objects, pk=kwargs.get("id"))
            Review.objects.create(
                star=form.data["star"],
                content=form.data["content"],
                category_id=form.data["category"],
                review_group_id_id=event.reviews.id,
                user_id=request.user.id,
            )
        return redirect("users:profile")
