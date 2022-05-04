from django.views.generic import TemplateView


class RatingTheatreView(TemplateView):
    template_name = 'rating/rating_theatre.html'


class RatingEventView(TemplateView):
    template_name = 'rating/rating_event.html'


class RatingCreateView(TemplateView):
    template_name = 'rating/rating_create.html'
