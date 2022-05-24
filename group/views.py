from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from group.models import MeetupParticipant
from theatres.forms import SearchForm
from theatres.models import Troupe
from users.models import add_experience

from .forms import MeetupForm
from .models import Meetup


class GroupListView(FormView):
    template_name = "group/group_list.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = kwargs.get("search_query", None)

        if search_query:
            context["meetups"] = Meetup.meetups.meetup_search(search_query)
            context["current_search"] = search_query
        else:
            context["meetups"] = Meetup.meetups.meetup_list()

        return context

    def form_valid(self, form, **kwargs):
        return self.render_to_response(self.get_context_data(search_query=form.data["search"]))


class GroupDetailView(View):
    @staticmethod
    def get(request, **kwargs):
        template = "group/group_detail.html"

        meetup = get_object_or_404(Meetup.meetups.meetup_details(kwargs["id"]))
        user = request.user

        return render(
            request,
            template,
            {
                "meetup": meetup,
                "actors": Troupe.troupes.fetch_members(meetup.event.troupe_id).prefetch_related("profile"),
                "is_participant": user in [participant.user for participant in meetup.participants.all()],
            },
        )

    @staticmethod
    def post(request, **kwargs):
        user = request.user
        meetup = get_object_or_404(Meetup, pk=kwargs["id"])

        if "group_delete" in request.POST:
            if meetup.host == user:
                meetup.delete()
                add_experience(user.id, -2)
            return redirect("group:group_list")
        elif "group_join" in request.POST:
            if not meetup.is_participant(user):
                MeetupParticipant.objects.create(meetup=meetup, user=user)
                add_experience(meetup.host_id, 15)
        elif "group_leave" in request.POST:
            if meetup.is_participant(user):
                MeetupParticipant.objects.filter(user=user, meetup=meetup).delete()

        return redirect("group:group_detail", meetup.id)


class GroupCreateView(TemplateView):
    template_name = "group/group_create.html"

    def get_context_data(self, **kwargs):
        form = MeetupForm()
        context = super().get_context_data(**kwargs)
        context["form"] = form
        return context

    @staticmethod
    def post(request):
        user = request.user

        form = MeetupForm(request.POST)
        meetup = form.save(commit=False)
        meetup.host = user
        meetup.save()
        add_experience(user.id, 5)

        return redirect("group:group_detail", meetup.id)
