from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets
from rest_framework.response import Response

from profiles.models import Profile
from skills.forms import SkillForm
from skills.models import Skill
from skills.serializers import SkillSerializer, SkillUpdateSerializer
from tshape.utils import MultiSerializerViewSetMixin


class SkillCreateView(CreateView):

    form_class = SkillForm
    template_name = 'skills/new.html'

    def form_valid(self, form, *args, **kwargs):
        skill = form.save(commit=False)
        skill.user = self.request.user
        self.kwargs['skill'] = skill.save()
        return super(SkillCreateView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        skill = self.kwargs.get('skill')
        return reverse('skills:detail', kwargs={'pk': skill.id})


class SkillDetailView(DetailView):

    model = Skill
    template_name = 'skills/detail.html'


class SkillListView(ListView):

    model = Skill
    template_name = 'skills/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SkillListView, self).get_context_data(*args, **kwargs)
        context.update(self.kwargs)
        context['object_list'] = Skill.objects.filter(skillset_id=self.kwar)
        return context


class SkillUpdateView(UpdateView):

    form_class = SkillForm
    template_name = 'skills/edit.html'

    def form_valid(self, form, *args, **kwargs):
        self.kwargs['skill'] = form.save()
        return super(SkillCreateView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        skill = self.kwargs.get('skill')
        return reverse('skills:detail', kwargs={'pk': skill.id})


class MultipleSkillsUpdateView(UpdateView):

    form_class = SkillForm
    template_name = 'skills/edit_all.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MultipleSkillsUpdateView, self
                        ).get_context_data(*args, **kwargs)
        context['profile_id'] = self.kwargs.get('profile_id')
        return context

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(pk=profile_id)
        return super(MultipleSkillsUpdateView, self
                     ).get_queryset().filter(profile=profile)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(MultipleSkillsUpdateView, self
                     ).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse(
            'skills:list', kwargs={'profile_id': self.request.user.id})


class SkillViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing skills.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    serializer_action_classes = {
        'list': SkillSerializer,
        'retrieve': SkillUpdateSerializer,
        'update': SkillUpdateSerializer,
        'partial_update': SkillUpdateSerializer,
        'destroy': SkillUpdateSerializer
    }

    def list(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_id)
        serializer_type = self.get_serializer_class()
        serializer = serializer_type(profile.skills, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        profile_id = self.kwargs.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_id)
        skill = get_object_or_404(profile.skills, pk=pk)
        serializer_type = self.get_serializer_class()
        serializer = serializer_type(skill)
        return Response(serializer.data)
