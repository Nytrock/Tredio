from django.urls import include, path

from .views import RatingCreateView, RatingEventView, RatingTheatreView

app_name = "rating"
urlpatterns = [
    path("event/<int:id>/", RatingEventView.as_view(), name="rating_event"),
    path("theatre/<int:id>/", RatingTheatreView.as_view(), name="rating_theatre"),
    path("create/<str:type>/<int:id>/", RatingCreateView.as_view(), name="rating_create"),
    path("__debug__/", include("debug_toolbar.urls")),
]
