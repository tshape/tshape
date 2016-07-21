from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from profiles.models import Profile
from skillsets.forms import SkillsetForm
from skillsets.models import Skillset
from skillsets.serializers import SkillsetSerializer, SkillsetUpdateSerializer
from tshape.utils import MultiSerializerViewSetMixin


class SkillsetCreateView(CreateView):

    form_class = SkillsetForm
    template_name = 'skillsets/new.html'

    def form_valid(self, form, *args, **kwargs):
        skillset = form.save(commit=False)
        skillset.user = self.request.user
        self.kwargs['skillset'] = skillset.save()
        return super(SkillsetCreateView, self
                     ).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        skillset = self.kwargs.get('skillset')
        return reverse('skillsets:detail', kwargs={
            'pk': skillset.id, 'profile_id': self.request.user.id})


class SkillsetDetailView(DetailView):

    model = Skillset
    template_name = 'skillsets/detail.html'
    fields = ['skillsets', 'skills']

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        if profile_id:
            return Profile.objects.get(pk=profile_id)
        return None


class SkillsetListView(ListView):

    model = Skillset
    template_name = 'skillsets/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            SkillsetListView, self).get_context_data(*args, **kwargs)
        context['profile_id'] = self.kwargs.get('profile_id')
        return context

    # def get_queryset(self):
    #     profile_id = self.kwargs.get('profile_id')
    #     return Profile.objects.get(pk=profile_id)
        # return super(
        #     SkillsetListView, self).get_queryset().filter(profile=profile)


class SkillsetUpdateView(UpdateView):

    form_class = SkillsetForm
    template_name = 'skillsets/edit.html'

    def form_valid(self, form, *args, **kwargs):
        self.kwargs['skillset'] = form.save()
        return super(SkillsetUpdateView, self
                     ).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        skillset = self.kwargs.get('skillset')
        return reverse('skillsets:detail', kwargs={
            'pk': skillset.id, 'profile_id': self.request.user.id})


class SkillsetViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing skillsets.
    """
    queryset = Skillset.objects.all()
    serializer_class = SkillsetSerializer
    serializer_action_classes = {
       'update': SkillsetUpdateSerializer,
       'partial_update': SkillsetUpdateSerializer,
       'destroy': SkillsetUpdateSerializer
    }
