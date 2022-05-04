from django.views.generic import TemplateView


class GroupListView(TemplateView):
    template_name = 'group/group_list.html'


class GroupDetailView(TemplateView):
    template_name = 'group/group_detail.html'


class GroupCreateView(TemplateView):
    template_name = 'group/group_create.html'
