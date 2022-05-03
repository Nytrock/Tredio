from django.urls import path, include

from .views import TheatresListView, TheatresDetailView, TheatresCreateView, \
    EventDetailView, EventCreateView

urlpatterns = [
    path('', TheatresListView.as_view(), name='theatres_list'),
    path('<int:id>/', TheatresDetailView.as_view(), name='theatres_detail'),
    path('create/', TheatresCreateView.as_view(), name='theatres_create'),
    path('events/<int:id>/', EventDetailView.as_view(), name='events_detail'),
    path('events/create/', EventCreateView.as_view(), name='events_create'),
    path('__debug__/', include('debug_toolbar.urls')),
]
