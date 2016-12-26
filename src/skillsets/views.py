from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView
)
from rest_framework import status, viewsets
from rest_framework.response import Response

from profiles.models import Profile, ProfileSkillset
from skillsets.forms import SkillsetForm
from skillsets.models import Skillset
from skillsets.serializers import (
    SkillsetSerializer, SkillsetUpdateSerializer, ProfileSkillsetSerializer
)
from tshape.utils import MultiSerializerViewSetMixin


class SkillsetViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):

    """A simple ViewSet for viewing and editing skillsets."""
    queryset = Skillset.objects.all()
    serializer_class = SkillsetSerializer
    serializer_action_classes = {
        'list': SkillsetSerializer,
        'update': SkillsetUpdateSerializer,
        'partial_update': SkillsetUpdateSerializer,
        'destroy': SkillsetUpdateSerializer
    }

    def get_serializer_context(self):
        context = super(SkillsetViewSet, self).get_serializer_context()
        if self.request.method in ['POST', 'PUT']:
            context['request'].data['id'] = self.kwargs.get(
                'pk', context['request'].data.get('id'))
        return context


class ProfileSkillsetViewSet(viewsets.ModelViewSet):

    """A simple ViewSet for viewing and editing skillsets."""
    queryset = ProfileSkillset.objects.all()
    serializer_class = ProfileSkillsetSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('pk')
        return get_object_or_404(
            ProfileSkillset,
            profile_id=profile_id, skillset_id=skillset_id)

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_pk')
        return ProfileSkillset.objects.filter(profile_id=profile_id)

    def get_serializer_context(self):
        context = super(ProfileSkillsetViewSet, self).get_serializer_context()
        if self.request.method in ['POST', 'PUT']:
            context['request'].data['profile_id'] = self.kwargs.get(
                'profile_pk', context['request'].data.get('profile_id'))
            context['request'].data['skillset_id'] = self.kwargs.get(
                'pk', context['request'].data.get('skillset_id'))
        return context

    def create(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.request.data.get('skillset_id')
        profile_weight = self.request.data.get('profile_weight')
        profile_skillset = ProfileSkillset.objects.create(
            profile_id=profile_id, skillset_id=skillset_id,
            profile_weight=profile_weight)
        serializer_cls = self.get_serializer_class()
        serializer = serializer_cls(profile_skillset, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('pk')
        skillset = get_object_or_404(Skillset, pk=skillset_id)
        weight = self.kwargs.get('weight', skillset.weight)
        profile_skillset = get_object_or_404(
            ProfileSkillset,
            profile_id=profile_id, skillset_id=skillset_id)
        profile_skillset.weight = weight
        return super(
            ProfileSkillsetViewSet, self).update(request, *args, **kwargs)


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
