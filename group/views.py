from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import MeetupForm
from .models import Meetup


class GroupListView(TemplateView):
    template_name = "group/group_list.html"


class GroupDetailView(TemplateView):
    template_name = "group/group_detail.html"


class GroupCreateView(View):
    def get(self, request):
        template = "group/group_create.html"
        form = MeetupForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, template, context)

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
