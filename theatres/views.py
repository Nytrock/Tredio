from django.views.generic import TemplateView


class TheatresListView(TemplateView):
    template_name = 'theatres/theatres_list.html'


class TheatresDetailView(TemplateView):
    template_name = 'theatres/theatres_detail.html'


class TheatresCreateView(TemplateView):
    template_name = 'theatres/theatres_create.html'


class EventDetailView(TemplateView):
    template_name = 'theatres/events_detail.html'


class EventCreateView(TemplateView):
    template_name = 'theatres/events_create.html'
