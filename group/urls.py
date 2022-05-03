from django.urls import path, include

from .views import GroupListView, GroupDetailView, GroupCreateView

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
    path('<int:id>/', GroupDetailView.as_view(), name='group_detail'),
    path('create/', GroupCreateView.as_view(), name='group_create'),
    path('__debug__/', include('debug_toolbar.urls')),
]
