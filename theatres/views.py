from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from core.forms import SearchForm
from core.models import City, ContactType
from rating.models import ReviewRating
from theatres.forms import ActorForm, EventForm, TheatreForm
from theatres.models import Event, Theatre, TroupeMember
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


class TheatresCreateView(LoginRequiredMixin, TemplateView):
    template_name = "theatres/theatres_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = TheatreForm()
        context["actors"] = ActorProfile.objects.filter(is_published=True)

        return context

    def post(self, request, *args, **kwargs):
        form = TheatreForm(request.POST, fields=request.POST.get("field_count"))

        if not form.is_valid():
            return self.render_to_response(context=dict(self.get_context_data(), form=form))
        form.save()

        return redirect("theatres:theatres_list")


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

        reviews = get_object_or_404(Event.events.event_ratings(kwargs["id"]))
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


class ActorCreateView(LoginRequiredMixin, TemplateView):
    template_name = "theatres/actors_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = ActorForm()
        context["contacts"] = ContactType.objects.all()
        context["id"] = kwargs.get("id")

        return context

    def post(self, request, *args, **kwargs):
        form = ActorForm(request.POST, request.FILES, fields=request.POST.get("field_count"))

        if not form.is_valid():
            return self.render_to_response(context=dict(self.get_context_data(), form=form))
        form.save()

        return redirect("homepage:home")


class EventCreateView(LoginRequiredMixin, TemplateView):
    template_name = "theatres/events_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = EventForm()
        context["actors"] = ActorProfile.objects.filter(is_published=True)

        return context

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST, request.FILES, fields=request.POST.get("field_count"))

        if not form.is_valid():
            return self.render_to_response(context=dict(self.get_context_data(), form=form))
        form.save()

        return redirect("theatres:events_list")
