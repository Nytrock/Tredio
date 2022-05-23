import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from rating.forms import RatingForm
from rating.models import Review, ReviewRating
from theatres.models import Event, Theatre
from users.models import add_experience


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class RatingTheatreView(View):
    def get(self, request, **kwargs):
        template = "rating/rating_theatre.html"
        context = {"reviews": get_object_or_404(Theatre.theatres.theatre_ratings(kwargs["id"]))}
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
        review_rating = ReviewRating.objects.filter(
            review_id=int(request.POST.get("id")), user_id=request.user.id
        ).prefetch_related("review")
        json_file = {
            "like": request.POST.get("like") == "True",
            "like_num": int(request.POST.get("like_num")),
            "dislike_num": int(request.POST.get("dislike_num")),
        }
        if review_rating:
            review_rating = review_rating.first()
            if review_rating.star == (request.POST.get("like") == "True"):
                if request.POST.get("like") == "True":
                    add_experience(review_rating.review.user_id, -2)
                else:
                    add_experience(review_rating.review.user_id, 2)
                review_rating.delete()
                return JsonResponse(json_file)
            else:
                if request.POST.get("like") == "True":
                    add_experience(review_rating.review.user_id, 2)
                else:
                    add_experience(review_rating.review.user_id, -2)
        review_rating = ReviewRating.objects.update_or_create(
            user_id=request.user.id,
            review_id=int(request.POST.get("id")),
            defaults={"star": request.POST.get("like") == "True"},
        )[0]
        if request.POST.get("like") == "True":
            add_experience(review_rating.review.user_id, 2)
        else:
            add_experience(review_rating.review.user_id, -2)

        return JsonResponse(json_file)


class RatingCreateView(TemplateView):
    template_name = "rating/rating_create.html"

    def get_context_data(self, **kwargs):
        form = RatingForm()

        context = super().get_context_data(**kwargs)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = RatingForm(request.POST)
        if kwargs.get("type") == "theatre":
            theatre = get_object_or_404(Theatre.objects, pk=kwargs.get("id"))
            Review.objects.create(
                star=request.POST.get("rating"),
                content=form.data["content"],
                category_id=form.data["category"],
                review_group_id_id=theatre.reviews.id,
                user_id=request.user.id,
            )
        else:
            event = get_object_or_404(Event.objects, pk=kwargs.get("id"))
            Review.objects.create(
                star=request.POST.get("rating"),
                content=form.data["content"],
                category_id=form.data["category"],
                review_group_id_id=event.reviews.id,
                user_id=request.user.id,
            )
        add_experience(request.user.id, 10)
        return redirect(f"rating:rating_{kwargs.get('type')}", kwargs.get("id"))
