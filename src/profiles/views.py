from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from rest_framework import viewsets, status
from rest_framework.response import Response

from profiles.forms import ProfileForm
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, ProfileUpdateSerializer
from skills.models import Skill
from skillsets.models import Skillset
from tshape.utils import MultiSerializerViewSetMixin


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


class ProfileViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    serializer_action_classes = {
       'update': ProfileUpdateSerializer,
       'partial_update': ProfileUpdateSerializer,
       'destroy': ProfileUpdateSerializer
    }
    # permission_classes = [IsAccountAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        data = request.data
        user_id = kwargs.get('pk')
        profile = Profile.objects.get(pk=user_id)

        with transaction.atomic():
            skillsets = data.pop('skillsets', None)
            if skillsets:
                ss_ids = [skillset['id'] for skillset in skillsets]
                profile.skillsets.set(Skillset.objects.filter(id__in=ss_ids))

            skills = data.pop('skills', None)
            if skills:
                s_ids = [skill['id'] for skill in skills]
                profile.skills.set(Skill.objects.filter(id__in=s_ids))

        serializer = ProfileUpdateSerializer(profile, data=data, partial=True)
        if serializer.is_valid(data):
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    # def partial_update(self, request, pk=None):
        # pass
