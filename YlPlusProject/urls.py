from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("homepage.urls")),
    path("group/", include("group.urls")),
    path("rating/", include("rating.urls")),
    path("theatres/", include("theatres.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
]
