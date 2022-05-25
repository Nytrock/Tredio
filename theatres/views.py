from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from core.forms import SearchForm
from core.models import City, Contact, ContactsGroup, ContactType, Location
from rating.models import ReviewGroup, ReviewRating
from theatres.forms import ActorForm, EventForm, TheatreForm
from theatres.models import Event, Theatre, Troupe, TroupeMember
from users.models import ActorProfile


class TheatresListView(FormView):
    template_name = "theatres/theatres_list.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = kwargs.get("search_query", None)

        if search_query:
            context["theatres"] = Theatre.theatres.theatre_search(search_query)
            context["current_search"] = search_query
        else:
            context["theatres"] = Theatre.theatres.theatres_list()
        context["cities"] = City.objects.all()

        return context

    def form_valid(self, form, **kwargs):
        return self.render_to_response(context=self.get_context_data(search_query=form.data["search"]))


class TheatresDetailView(TemplateView):
    template_name = "theatres/theatres_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["theatre"] = get_object_or_404(Theatre.theatres.theatre_details(kwargs["id"]))
        context["actors"] = TroupeMember.objects.filter(
            troupe=context["theatre"].troupe, profile__is_published=True
        ).prefetch_related("profile")

        return context


class TheatresCreateView(FormView):
    template_name = "theatres/theatres_create.html"
    form_class = TheatreForm
    success_url = "theatres:theatres_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TheatreForm()
        context["actors"] = ActorProfile.objects.filter(is_published=True)
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def form_valid(self, form):
        num = 1
        troupe_data = {}
        while True:
            try:
                actor = form.data["actor_change" + str(num)]
            except:
                break
            try:
                role = form.data["role" + str(num)]
            except:
                role = ""
            troupe_data[actor] = role
            num += 1
        reviews = ReviewGroup.objects.create()
        troupe = Troupe.objects.create()
        for name in troupe_data:
            actor = ActorProfile.objects.filter(first_name=name.split()[0], last_name=name.split()[1]).first()
            TroupeMember.objects.create(profile_id=actor.id, troupe_id=troupe.id, role=troupe_data[name])

        location, _ = Location.objects.get_or_create(
            query=form.cleaned_data["address"],
            city=City.objects.get_or_create(name=form.cleaned_data["city"])[0],
            fias=form.cleaned_data["fias"],
        )

        theatre = form.save(commit=False)

        theatre.troupe = troupe
        theatre.reviews = reviews
        theatre.location = location
        theatre.contacts = ContactsGroup.objects.create()

        theatre.save()
        return redirect(TheatresCreateView.success_url)


class EventListView(FormView):
    template_name = "theatres/events_list.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = kwargs.get("search_query", None)

        if search_query:
            context["events"] = Event.events.event_search(search_query)
            context["current_search"] = search_query
        else:
            context["events"] = Event.events.events_list()
        context["cities"] = City.objects.all()

        return context

    def form_valid(self, form, **kwargs):
        return self.render_to_response(context=self.get_context_data(search_query=form.data["search"]))


class EventDetailView(View):
    def get(self, request, **kwargs):
        template = "theatres/events_detail.html"
        user = request.user

        reviews = get_object_or_404(Theatre.theatres.theatre_ratings(kwargs["id"]))
        event = get_object_or_404(Event.events.event_details(kwargs["id"]))

        for review in reviews.reviews.reviews.all():
            review.user_like = user in [review.user for review in review.like]
            review.user_dislike = user in [review.user for review in review.dislike]

        return render(
            request,
            template,
            {
                "reviews": reviews,
                "event": event,
                "actors": TroupeMember.objects.filter(troupe=event.troupe).prefetch_related("profile"),
            },
        )

    @staticmethod
    def post(request, **kwargs):
        review_id = int(request.POST.get("id"))
        like = request.POST.get("like") == "True"
        review = ReviewRating.objects.filter(review_id=review_id).first()

        json_file = {
            "like": like,
            "like_num": int(request.POST.get("like_num")),
            "dislike_num": int(request.POST.get("dislike_num")),
        }

        if review and review.star == like:
            review.delete()
        else:
            ReviewRating.objects.update_or_create(
                user_id=request.user.id,
                review_id=review_id,
                defaults={"star": like},
            )

        return JsonResponse(json_file)


class ActorCreateView(FormView):
    template_name = "theatres/actors_create.html"
    form_class = ActorForm
    success_url = "theatres:events_list"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["contacts"] = ContactType.objects.all()
        context["id"] = kwargs.get("id")
        return self.render_to_response(context)

    def form_valid(self, form):
        num = 1
        contact_data = {}
        while True:
            try:
                actor = form.data["contact_type" + str(num)]
            except:
                break
            try:
                role = form.data["value" + str(num)]
            except:
                break
            contact_data[actor] = role
            num += 1
        group = ContactsGroup.objects.create()
        for name in contact_data:
            contact_type = ContactType.objects.filter(name=name).first()
            Contact.objects.create(
                value=contact_data[name],
                type_id=contact_type.id,
                contacts_group_id=group.id,
            )
        new_actor = form.save(commit=False)
        new_actor.contacts = group
        new_actor.save()
        return redirect("homepage:home")


class EventCreateView(FormView):
    template_name = "theatres/events_create.html"
    form_class = EventForm
    success_url = "theatres:events_list"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["actors"] = ActorProfile.objects.filter(is_published=True)
        return self.render_to_response(context)

    def form_valid(self, form):
        num = 1
        troupe_data = {}
        while True:
            try:
                actor = form.data["actor_change" + str(num)]
            except:
                break
            try:
                role = form.data["role" + str(num)]
            except:
                role = ""
            troupe_data[actor] = role
            num += 1
        reviews = ReviewGroup.objects.create()
        troupe = Troupe.objects.create()
        for name in troupe_data:
            actor = ActorProfile.objects.filter(first_name=name.split()[0], last_name=name.split()[1]).first()
            TroupeMember.objects.create(profile_id=actor.id, troupe_id=troupe.id, role=troupe_data[name])
        event = form.save(commit=False)
        event.troupe = troupe
        event.reviews = reviews
        event.save()
        return redirect("theatres:events_list")
