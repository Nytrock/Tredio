from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from group.models import MeetupParticipant
from theatres.models import Event, TroupeMember
from users.models import UserProfile, add_experience

from .forms import MeetupForm
from .models import Meetup


class GroupListView(TemplateView):
    template_name = "group/group_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meetups"] = Meetup.meetups.meetup_list()
        return context


class GroupDetailView(View):
    def get(self, request, **kwargs):
        template = "group/group_detail.html"
        context = {"meetup": get_object_or_404(Meetup.meetups.meetup_details(kwargs["id"]))}
        context["actors"] = TroupeMember.objects.filter(troupe=context["meetup"].event.troupe_id).prefetch_related(
            "profile"
        )
        in_meetup = False
        for participant in context["meetup"].participants.all():
            if participant.user_id == request.user.id:
                in_meetup = True
        context["in_meetup"] = in_meetup
        return render(request, template, context)

    def post(self, request, **kwargs):
        if request.POST.get("group_delete") is not None:
            Meetup.objects.filter(id=kwargs["id"]).delete()
            add_experience(request.user.id, -2)
            return redirect("group:group_list")
        if request.POST.get("group_add") == "True":
            meetup = get_object_or_404(Meetup, pk=kwargs["id"])
            MeetupParticipant.objects.create(meetup_id=meetup.id, user_id=request.user.id)
            add_experience(meetup.host_id, 15)
        else:
            MeetupParticipant.objects.filter(user_id=request.user.id).delete()
        return redirect("group:group_detail", kwargs["id"])


class GroupCreateView(TemplateView):
    template_name = "group/group_create.html"

    def get_context_data(self, **kwargs):
        form = MeetupForm()
        context = super().get_context_data(**kwargs)
        context["form"] = form
        return context

    def post(self, request):
        add_experience(request.user.id, 5)
        form = MeetupForm(request.POST)
        meetup = form.save(commit=False)
        meetup.host_id = request.user.id
        meetup.save()
        return redirect("group:group_detail", meetup.id)
