from rest_framework import serializers

from profiles.models import Profile
from skills.serializers import SkillSerializer
from skillsets.serializers import SkillsetSerializer
from users.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    skills = SkillSerializer(many=True)
    skillsets = SkillsetSerializer(many=True)
    # skill_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # skillset_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'title', 'description',
                  'years_experience', 'skills', 'skillsets')  # , 'skill_ids', 'skillset_ids')


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'title', 'description',
                  'years_experience', 'skill_ids', 'skillset_ids')
        read_only_fields = ('user_id',)
