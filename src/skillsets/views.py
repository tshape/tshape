from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from profiles.models import Profile
from skillsets.forms import SkillsetForm
from skillsets.models import Skillset
from skillsets.serializers import SkillsetSerializer
from tshape.utils import PKContextMixin


class SkillsetCreateView(CreateView):

    form_class = SkillsetForm
    template_name = 'skillsets/new.html'

    def form_valid(self, form, *args, **kwargs):
        skillset = form.save(commit=False)
        skillset.user = self.request.user
        skillset.save()
        return reverse('skillsets:detail', kwargs={'pk': skillset.id})


class SkillsetDetailView(DetailView):

    model = Skillset
    template_name = 'skillsets/detail.html'
    fields = ['skillsets', 'skills']

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        if profile_id:
            return Profile.objects.get(pk=profile_id)
        return None


class SkillsetListView(PKContextMixin, ListView):

    model = Skillset
    template_name = 'skillsets/list.html'


class SkillsetUpdateView(UpdateView):

    form_class = SkillsetForm
    template_name = 'skillsets/edit.html'

    def form_valid(self, form, *args, **kwargs):
        skillset = form.save()
        return reverse('skillsets:detail', kwargs={'pk': skillset.id})


class ProfileSkillsetsUpdateView(PKContextMixin, UpdateView):

    template_name = 'skillsets/edit.html'
    fields = ['skillsets', 'skills']

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        return Profile.objects.get(pk=profile_id)


class SkillsetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Skillset.objects.all()
    serializer_class = SkillsetSerializer
