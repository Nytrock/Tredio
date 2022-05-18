from django.urls import include, path

from .views import HomeView

app_name = "homepage"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("__debug__/", include("debug_toolbar.urls")),
]
