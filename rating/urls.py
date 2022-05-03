from django.urls import path, include

from .views import RatingTheatreView, RatingEventView, RatingCreateView

urlpatterns = [
    path('event/<int:id>/', RatingEventView.as_view(), name='rating_event'),
    path('theatre/<int:id>/', RatingTheatreView.as_view(), name='rating_theatre'),
    path('create/', RatingCreateView.as_view(), name='rating_create'),
    path('__debug__/', include('debug_toolbar.urls')),
]
