from django.urls import include, path

from .views import RatingCreateView, RatingTheatreView

app_name = "rating"
urlpatterns = [
    path("theatre/<int:id>/", RatingTheatreView.as_view(), name="rating_theatre"),
    path("create/<str:type>/<int:id>/", RatingCreateView.as_view(), name="rating_create"),
    path("__debug__/", include("debug_toolbar.urls")),
]
