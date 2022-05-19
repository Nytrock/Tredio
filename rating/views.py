from django.views.generic import TemplateView


class RatingTheatreView(TemplateView):
    template_name = "rating/rating_theatre.html"


class RatingEventView(TemplateView):
    template_name = "rating/rating_event.html"


class RatingCreateView(TemplateView):
    template_name = "rating/rating_create.html"

    def get_context_data(self, **kwargs):
        # Replace None with real form

        context = super().get_context_data(**kwargs)
        context["form"] = None
        return context
