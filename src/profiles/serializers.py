from rest_framework import serializers

from profiles.models import Profile
from skills.serializers import SkillNestedSerializer
from skillsets.serializers import SkillsetNestedSerializer


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'skillsets', 'skills')
        read_only_fields = ('user_id', 'skillsets', 'skills')

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    skillsets = SkillsetNestedSerializer(many=True, required=False)
    skills = SkillNestedSerializer(many=True, required=False)


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'skillsets', 'skills')
        read_only_fields = ('user_id', 'skillsets', 'skills')

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)
    skillsets = SkillsetNestedSerializer(many=True, required=False)
    skills = SkillNestedSerializer(many=True, required=False)
