from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets
from rest_framework.response import Response

from profiles.models import Profile, ProfileSkillset
from skillsets.forms import SkillsetForm
from skillsets.models import Skillset
from skillsets.serializers import (
    SkillsetSerializer, SkillsetUpdateSerializer, ProfileSkillsetSerializer
)


class SkillsetViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing skillsets.
    """
    queryset = Skillset.objects.all()
    serializer_class = SkillsetSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('pk')
        if profile_id:
            return get_object_or_404(
                ProfileSkillset,
                profile_id=profile_id, skillset_id=skillset_id)
        else:
            return get_object_or_404(Skillset, pk=skillset_id)

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('pk')
        if profile_id and skillset_id:
            return get_object_or_404(
                ProfileSkillset,
                profile_id=profile_id, skillset_id=skillset_id)
        elif profile_id:
            return ProfileSkillset.objects.filter(profile_id=profile_id)
        return super(SkillsetViewSet, self).get_queryset()

    def get_serializer_class(self):
        if self.kwargs.get('profile_pk'):
            return ProfileSkillsetSerializer
        elif not self.kwargs.get('pk'):
            return SkillsetSerializer
        else:
            return SkillsetUpdateSerializer

    def create(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        skillset_id = self.kwargs.get('pk')
        weight = self.kwargs.get('weight', None)
        if profile_id:
            return ProfileSkillset.objects.create(
                profile_id=profile_id, skillset_id=skillset_id, weight=weight)
        return super(SkillsetViewSet, self).create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        skillset_id = self.kwargs.get('pk')
        weight = self.kwargs.get('weight', None)
        if profile_id:
            profile_skillset = get_object_or_404(
                ProfileSkillset,
                profile_id=profile_id, skillset_id=skillset_id)
            profile_skillset.weight = weight
            return profile_skillset.save()
        return super(SkillsetViewSet, self).update(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     profile_id = self.kwargs.get('profile_pk')
    #     if profile_id:
    #         skillsets = get_object_or_404(Profile, pk=profile_id).skillsets
    #     else:
    #         skillsets = Skillset.objects.all()
    #     serializer_type = self.get_serializer_class()
    #     serializer = serializer_type(skillsets, many=True)
    #     return ResAponse(serializer.data)

    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     profile_id = self.kwargs.get('profile_pk')
    #     if profile_id:
    #         profile = get_object_or_404(Profile, pk=profile_id)
    #         skillset = get_object_or_404(profile.skillsets, pk=pk)
    #     else:
    #         skillset = Skillset.objects.get(pk=pk)
    #     serializer_type = self.get_serializer_class()
    #     serializer = serializer_type(skillset)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     data = request.data
    #     skillset_id = kwargs.get('pk')
    #     skillset = Skillset.objects.get(pk=skillset_id)

    #     with transaction.atomic():
    #         skills = data.pop('skills', None)
    #         if skills:
    #             sids = [skill['id'] for skill in skills]
    #             skillset.skills.set(Skill.objects.filter(id__in=sids))

    #     serializer_type = self.get_serializer_class()
    #     serializer = serializer_type(skillset, data=data, partial=True)
    #     if serializer.is_valid(data):
    #         serializer.update(skillset, data)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK,
    #                     headers=headers)


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
