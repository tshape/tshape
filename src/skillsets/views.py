from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets

from profiles.models import Profile
from skillsets.forms import SkillsetForm, SkillsetFormSet
from skillsets.models import Skillset
from skillsets.serializers import SkillsetSerializer
from tshape.utils import PKContextMixin


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

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(pk=profile_id)
        return super(
            SkillsetListView, self).get_queryset().filter(profile=profile)


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


class MultipleSkillsetsUpdateView(UpdateView):

    form_class = SkillsetFormSet
    template_name = 'skillsets/edit_all.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MultipleSkillsetsUpdateView, self
                        ).get_context_data(*args, **kwargs)
        context['profile_id'] = self.kwargs.get('profile_id')
        print(context)
        # context['formset'] = SkillsetFormSet
        return context

    # def get_queryset(self):
    #     profile_id = self.kwargs.get('profile_id')
    #     profile = Profile.objects.get(pk=profile_id)
    #     return Skillset.objects.filter(profile=profile)
    #     # return super(MultipleSkillsetsUpdateView, self
    #     #              ).get_queryset().filter(profile=profile)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(MultipleSkillsetsUpdateView, self
                     ).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('skillsets:list',
                       kwargs={'profile_id': self.request.user.id})


class SkillsetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Skillset.objects.all()
    serializer_class = SkillsetSerializer
