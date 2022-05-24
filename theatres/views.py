from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from core.models import Contact, ContactsGroup, ContactType
from rating.models import ReviewGroup, ReviewRating
from theatres.forms import ActorForm, EventForm, TheatreForm
from theatres.models import City, Event, Theatre, Troupe, TroupeMember
from users.models import ActorProfile, add_experience


class TheatresListView(TemplateView):
    template_name = "theatres/theatres_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theatres"] = Theatre.theatres.theatres_list()
        context["cities"] = City.objects.all()
        return context


class TheatresDetailView(TemplateView):
    template_name = "theatres/theatres_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theatre"] = get_object_or_404(Theatre.theatres.theatre_details(kwargs["id"]))
        context["actors"] = TroupeMember.objects.filter(troupe=context["theatre"].troupe_id).prefetch_related("profile")
        return context


class TheatresCreateView(TemplateView):
    template_name = "theatres/theatres_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TheatreForm()
        context["actors"] = ActorProfile.objects.filter(is_published=True)
        return context


class EventListView(TemplateView):
    template_name = "theatres/events_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.events.events_list()
        context["cities"] = City.objects.all()
        return context


class EventDetailView(View):
    def get(self, request, **kwargs):
        template = "theatres/events_detail.html"
        context = {
            "reviews": get_object_or_404(Event.events.event_ratings(kwargs["id"])),
            "event": get_object_or_404(Event.events.event_details(kwargs["id"])),
        }
        context["actors"] = TroupeMember.objects.filter(troupe=context["event"].troupe_id).prefetch_related("profile")
        self.user = request.user.id
        for review in context["reviews"].reviews.reviews.all():
            like = False
            dislike = False
            for rat in review.like:
                if rat.user_id == self.user:
                    like = True
            for rat in review.dislike:
                if rat.user_id == self.user:
                    dislike = True
            review.user_like = like
            review.user_dislike = dislike
        return render(request, template, context)

    def post(self, request, **kwargs):
        review = ReviewRating.objects.filter(review_id=int(request.POST.get("id")))
        json_file = {
            "like": request.POST.get("like") == "True",
            "like_num": int(request.POST.get("like_num")),
            "dislike_num": int(request.POST.get("dislike_num")),
        }
        if review:
            if review.first().star == (request.POST.get("like") == "True"):
                review.delete()
                return JsonResponse(json_file)
        ReviewRating.objects.update_or_create(
            user_id=request.user.id,
            review_id=int(request.POST.get("id")),
            defaults={"star": request.POST.get("like") == "True"},
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
                contacts_group_id_id=group.id,
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
