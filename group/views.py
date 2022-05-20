from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from group.models import Meetup

from .forms import MeetupForm
from .models import Meetup


class GroupListView(TemplateView):
    template_name = "group/group_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meetups"] = Meetup.meetups.meetup_list()
        return context


class GroupDetailView(TemplateView):
    template_name = "group/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meetup"] = get_object_or_404(Meetup.meetups.meetup_details(kwargs["id"]))
        return context


class GroupCreateView(TemplateView):
    template_name = "group/group_create.html"

    def get_context_data(self, **kwargs):
        form = MeetupForm()
        context = super().get_context_data(**kwargs)
        context["form"] = form
        return context

    def post(self, request):
        form = MeetupForm(request.POST)
        if form.data[Meetup.participants_limit.field.name] != "":
            Meetup.objects.create(
                event_id=form.data[Meetup.event.field.name],
                start=form.data[Meetup.start.field.name],
                participants_limit=form.data[Meetup.participants_limit.field.name],
                description=form.data[Meetup.description.field.name],
                host_id=request.user.id,
            )
        else:
            Meetup.objects.create(
                event_id=form.data[Meetup.event.field.name],
                start=form.data[Meetup.start.field.name],
                description=form.data[Meetup.description.field.name],
                host_id=request.user.id,
            )
        return redirect("group:group_list")
