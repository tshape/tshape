from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from profiles.forms import ProfileForm
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from skills.models import Skill
from skillsets.models import Skillset
from users.models import User


class ProfileDetailView(DetailView):

    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        if profile_id:
            return Profile.objects.get(pk=profile_id)
        return self.request.user.profile


class ProfileListView(ListView):

    model = Profile
    template_name = 'profiles/list.html'


class ProfileUpdateView(UpdateView):

    form_class = ProfileForm
    template_name = 'profiles/edit.html'

    def get_object(self, *args, **kwargs):
        profile_id = self.kwargs.get('profile_id')
        return Profile.objects.get(pk=profile_id)

    def form_valid(self, form, *args, **kwargs):
        form.save()
        return super(ProfileUpdateView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('profiles:detail',
                       kwargs={'profile_id': self.request.user.id})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        data = request.data
        profile = Profile.objects.get(pk=data['user_id'])

        with transaction.atomic():
            profile.first_name = data.get('first_name', profile.first_name)
            profile.last_name = data.get('last_name', profile.last_name)
            profile.title = data.get('title', profile.title)
            profile.description = data.get('description', profile.description)
            profile.years_experience = data(
                'years_experience', profile.years_experience)
            profile.full_clean()
            profile.save()

            if data.get('skillsets'):
                profile.skillsets = Skillset.objects.get(
                    pk__in=[data['skillsets']])

            if data.get('skills'):
                profile.skills = Skill.objects.get(pk__in=[data['skills']])
            profile.save()

        serializer = self.serializer_class(profile, partial=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
