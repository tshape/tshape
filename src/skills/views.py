from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets, status
from rest_framework.response import Response

from profiles.models import Profile, ProfileSkill
from skills.forms import SkillForm
from skills.models import Skill
from skills.serializers import (
    SkillSerializer, SkillUpdateSerializer, ProfileSkillSerializer
)
from skillsets.models import Skillset


class SkillViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing skills.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    # lookup_url_kwarg = ('profile_pk', 'skillset_pk')

    def get_object(self):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('skillset_pk')
        skill_id = self.kwargs.get('pk')
        if profile_id and skill_id:
            return get_object_or_404(
                ProfileSkill, profile_id=profile_id, skill_id=skill_id)
        elif skillset_id:
            return get_object_or_404(
                Skill, pk=skill_id, skillset_id=skillset_id)
        else:
            return get_object_or_404(Skill, id=skill_id)

    def get_queryset(self):
        print("in get_queryset")
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('skillset_pk')
        print("profile_id: ", profile_id)
        print("skillset_id: ", skillset_id)
        if profile_id and skillset_id:
            query = ProfileSkill.objects.filter(profile_id=profile_id)
            print([skill for skill in query if skill.skillset_id == skillset_id])
            return [
                skill for skill in query if skill.skillset_id == skillset_id]
        elif profile_id:
            return ProfileSkill.objects.filter(profile_id=profile_id)
        elif skillset_id:
            return get_object_or_404(Skillset, pk=skillset_id).skills
        else:
            return super(SkillViewSet, self).get_queryset()

    def get_serializer_class(self):
        if self.kwargs.get('profile_pk'):
            return ProfileSkillSerializer
        elif not self.kwargs.get('pk'):
            return SkillSerializer
        else:
            return SkillUpdateSerializer

    def create(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        skillset_id = self.kwargs.get('skillset_pk')
        skill_id = self.kwargs.get('pk')
        weight = self.kwargs.get('weight', None)
        if profile_id:
            return ProfileSkill.objects.create(
                profile_id=profile_id, skill_id=skill_id, weight=weight)
        elif skillset_id:
            request.data['skillset_id'] = skillset_id
        return super(SkillViewSet, self).create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        skillset_id = self.kwargs.get('skillset_pk')
        skill_id = self.kwargs.get('pk')
        weight = self.kwargs.get('weight', None)
        if profile_id:
            profile_skill = get_object_or_404(
                ProfileSkill, profile_id=profile_id, skill_id=skill_id)
            profile_skill.weight = weight
            return profile_skill.save()
        elif skillset_id:
            request.data['skillset_id'] = skillset_id
        return super(SkillViewSet, self).update(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     serializer_type = self.get_serializer_class()
    #     skills = self.get_queryset()
    #     if self.kwargs.get('profile_pk'):
    #         serializer_type = ProfileSkillSerializer
    #     serializer = serializer_type(skills, many=True)
    #     return Response(serializer.data)


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
