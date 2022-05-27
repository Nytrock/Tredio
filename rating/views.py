from django.core.exceptions import BadRequest
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
        user = request.user
        reviews = get_object_or_404(Theatre.theatres.theatre_ratings(kwargs["id"]))

        for review in reviews.reviews.reviews.all():
            review.user_like = user in [review.user for review in review.like]
            review.user_dislike = user in [review.user for review in review.dislike]

        return render(request, template, {"reviews": reviews})

    @staticmethod
    def post(request, **kwargs):
        user = request.user
        like = request.POST.get("like") == "True"

        review_rating = (
            ReviewRating.objects.filter(review_id=int(request.POST.get("id")), user_id=user.id)
            .prefetch_related("review")
            .first()
        )
        json_file = {
            "like": like,
            "like_num": int(request.POST.get("like_num")),
            "dislike_num": int(request.POST.get("dislike_num")),
        }

        if review_rating:
            star = review_rating.star
            modifier = 1 if (like == (star == like)) else -1
            add_experience(review_rating.review.user_id, 2 * modifier)
            if like == star:
                review_rating.delete()
                return JsonResponse(json_file)

        review_rating, _ = ReviewRating.objects.update_or_create(
            user_id=user.id,
            review_id=int(request.POST.get("id")),
            defaults={"star": like},
        )
        add_experience(review_rating.review.user_id, 2 * (1 if like else -1))

        return JsonResponse(json_file)


class RatingCreateView(TemplateView):
    template_name = "rating/rating_create.html"

    def get_context_data(self, **kwargs):
        form = RatingForm()

        context = super().get_context_data(**kwargs)
        context["form"] = form
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        form = RatingForm(request.POST)
        review_type = kwargs.get("type")
        object_id = kwargs.get("id")
        
        redirect_url = {"event": "theatres:events_detail", "theatre": "rating:rating_theatre"}

        if review_type in ["event", "theatre"]:
            manager = Theatre.objects if review_type == "theatre" else Event.objects
            obj = get_object_or_404(manager, pk=object_id)

            Review.objects.create(
                star=request.POST.get("rating"),
                content=form.data["content"],
                category_id=form.data["category"],
                review_group_id_id=obj.reviews.id,
                user_id=request.user.id,
            )
            add_experience(request.user.id, 10)
            return redirect(redirect_url[review_type], object_id)

        raise BadRequest()