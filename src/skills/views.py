from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from profiles.models import ProfileSkill
from skills.models import Skill
from skills.serializers import (
    SkillSerializer, SkillUpdateSerializer, ProfileSkillSerializer
)
from skillsets.models import Skillset
from tshape.utils import MultiSerializerViewSetMixin


class SkillViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing skills.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    serializer_action_classes = {
        'list': SkillSerializer,
        'update': SkillUpdateSerializer,
        'partial_update': SkillUpdateSerializer,
        'destroy': SkillUpdateSerializer
    }

    def get_object(self):
        skillset_id = self.kwargs.get('skillset_pk')
        skill_id = self.kwargs.get('pk')
        if skillset_id:
            return get_object_or_404(
                Skill, pk=skill_id, skillset_id=skillset_id)
        else:
            return super(SkillViewSet, self).get_object()

    def get_queryset(self):
        skillset_id = self.kwargs.get('skillset_pk')
        if skillset_id:
            return get_object_or_404(Skillset, pk=skillset_id).skills
        else:
            return super(SkillViewSet, self).get_queryset()

    def get_serializer_context(self):
        context = super(SkillViewSet, self).get_serializer_context()
        if self.request.method in ['POST', 'PUT']:
            context['request'].data['skillset_id'] = self.kwargs.get(
                'skillset_pk', context['request'].data.get('skillset_id'))
            context['request'].data['id'] = self.kwargs.get(
                'pk', context['request'].data.get('id'))
        return context

    # def filter_queryset(self, queryset):
    #     print(queryset)
    #     filter_backend = SkillFilter
    #     print(filter_backend.__dict__)
    #     if 'profile_pk' in self.request.query_params:
    #         filter_backend = ProfileSkillFilter
    #     queryset = filter_backend().filter_queryset(
    #         self.request, self.get_queryset(), view=self)
    #     return queryset

    # def create(self, request, *args, **kwargs):
    #     skillset_id = self.kwargs.get('skillset_pk')
    #     # skill_id = self.kwargs.get('pk')
    #     # weight = self.kwargs.get('weight')
    #     if skillset_id:
    #         request.data['skillset_id'] = skillset_id
    #     return super(SkillViewSet, self).create(request, *args, **kwargs)

    # def update(self, request, pk=None, *args, **kwargs):
    #     skillset_id = self.kwargs.get('skillset_pk')
    #     # skill_id = self.kwargs.get('pk')
    #     # weight = self.kwargs.get('weight')
    #     if skillset_id:
    #         request.data['skillset_id'] = skillset_id
    #     return super(SkillViewSet, self).update(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     serializer_type = self.get_serializer_class()
    #     skills = self.get_queryset()
    #     if self.kwargs.get('profile_pk'):
    #         serializer_type = ProfileSkillSerializer
    #     serializer = serializer_type(skills, many=True)
    #     return Response(serializer.data)


class ProfileSkillViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing profile skills.
    """
    queryset = ProfileSkill.objects.all()
    serializer_class = ProfileSkillSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_pk')
        skill_id = self.kwargs.get('pk')
        return get_object_or_404(
            ProfileSkill, profile_id=profile_id, skill_id=int(skill_id))

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_pk')
        skillset_id = self.kwargs.get('skillset_pk')
        if skillset_id:
            return ProfileSkill.objects.filter(
                profile_id=profile_id, skill__skillset_id=skillset_id)
        else:
            return ProfileSkill.objects.filter(profile_id=profile_id)

    def get_serializer_context(self):
        context = super(ProfileSkillViewSet, self).get_serializer_context()
        if self.request.method in ['POST', 'PUT']:
            context['request'].data['profile_id'] = self.kwargs.get(
                'profile_pk', context['request'].data.get('profile_id'))
            context['request'].data['skill_id'] = self.kwargs.get(
                'pk', context['request'].data.get('skill_id'))
        return context

    def create(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('profile_pk')
        skill_id = self.request.data.get('skill_id')
        profile_weight = self.request.data.get('profile_weight')
        profile_skill = ProfileSkill.objects.create(
            profile_id=profile_id, skill_id=skill_id,
            profile_weight=profile_weight)
        serializer_cls = self.get_serializer_class()
        serializer = serializer_cls(profile_skill, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SkillCreateView(CreateView):

#     form_class = SkillForm
#     template_name = 'skills/new.html'

#     def form_valid(self, form, *args, **kwargs):
#         skill = form.save(commit=False)
#         skill.user = self.request.user
#         self.kwargs['skill'] = skill.save()
#         return super(SkillCreateView, self).form_valid(form, *args, **kwargs)

#     def get_success_url(self, *args, **kwargs):
#         skill = self.kwargs.get('skill')
#         return reverse('skills:detail', kwargs={'pk': skill.id})


# class SkillDetailView(DetailView):

#     model = Skill
#     template_name = 'skills/detail.html'


# class SkillListView(ListView):

#     model = Skill
#     template_name = 'skills/list.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(SkillListView, self).get_context_data(*args, **kwargs)
#         context.update(self.kwargs)
#         context['object_list'] = Skill.objects.filter(skillset_id=self.kwar)
#         return context


# class SkillUpdateView(UpdateView):

#     form_class = SkillForm
#     template_name = 'skills/edit.html'

#     def form_valid(self, form, *args, **kwargs):
#         self.kwargs['skill'] = form.save()
#         return super(SkillCreateView, self).form_valid(form, *args, **kwargs)

#     def get_success_url(self, *args, **kwargs):
#         skill = self.kwargs.get('skill')
#         return reverse('skills:detail', kwargs={'pk': skill.id})


# class MultipleSkillsUpdateView(UpdateView):

#     form_class = SkillForm
#     template_name = 'skills/edit_all.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(MultipleSkillsUpdateView, self
#                         ).get_context_data(*args, **kwargs)
#         context['profile_id'] = self.kwargs.get('profile_id')
#         return context

#     def get_queryset(self):
#         profile_id = self.kwargs.get('profile_id')
#         profile = Profile.objects.get(pk=profile_id)
#         return super(MultipleSkillsUpdateView, self
#                      ).get_queryset().filter(profile=profile)

#     def form_valid(self, form, *args, **kwargs):
#         form.save()
#         return super(MultipleSkillsUpdateView, self
#                      ).form_valid(form, *args, **kwargs)

#     def get_success_url(self, *args, **kwargs):
#         return reverse(
#             'skills:list', kwargs={'profile_id': self.request.user.id})
