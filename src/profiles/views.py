from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from skills.models import Skill
from skillsets.models import Skillset
from tshape.utils import MultiSerializerViewSetMixin


class ProfileViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):

    """A simple ViewSet for viewing and editing profiles."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'head', 'put', 'delete']
    # permission_classes = [IsAccountAdminOrReadOnly]

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
