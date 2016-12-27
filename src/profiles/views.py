from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, UpdateView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from profiles.forms import ProfileForm
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from skills.models import Skill
from skillsets.models import Skillset
from tshape.utils import (
    MultiSerializerViewSetMixin, LoggedInMixin, StaffRequiredMixin
)
from users.models import User


class ProfileViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):

    """A simple ViewSet for viewing and editing profiles."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'head', 'put', 'delete']
    permission_classes = [IsAdminUser]

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data
        profile = Profile.objects.get(pk=pk)

        with transaction.atomic():
            skillset_ids = data.pop('skillset_ids', None)
            if skillset_ids:
                profile.skillsets.set(
                    Skillset.objects.filter(id__in=skillset_ids))

            skill_ids = data.pop('skill_ids', None)
            if skill_ids:
                profile.skills.set(Skill.objects.filter(id__in=skill_ids))

        serializer_type = self.get_serializer_class()
        serializer = serializer_type(profile, data=data, partial=True)
        if serializer.is_valid(data):
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class ProfileDetailView(LoggedInMixin, DetailView):

    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return get_object_or_404(Profile, pk=user.id)
        return self.request.user.profile


class ProfileListView(StaffRequiredMixin, ListView):

    model = Profile
    template_name = 'profiles/list.html'


class ProfileUpdateView(LoggedInMixin, UpdateView):

    form_class = ProfileForm
    template_name = 'profiles/edit.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return get_object_or_404(Profile, pk=user.id)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(ProfileUpdateView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('profiles:detail',
                       kwargs={'profile_id': self.request.user.id})
