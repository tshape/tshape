from rest_framework import serializers

from profiles.models import ProfileSkill
from skills.models import Skill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'weight',
                  'skillset_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    skillset_id = serializers.IntegerField()


class SkillUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'weight',
                  'skillset_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'skillset_id', 'created_at', 'updated_at')

    skillset_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    name = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False)


class SkillNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'weight',
                  'skillset_id', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'name', 'description', 'verified', 'weight',
            'skillset_id', 'created_at', 'updated_at')

    skillset_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    name = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False)


class ProfileSkillSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileSkill
        fields = ('id', 'name', 'description', 'verified', 'weight',
                  'skillset_id', 'created_at', 'updated_at')
        read_only_fields = (
            'id', 'name', 'description', 'verified', 'weight',
            'skillset_id', 'created_at', 'updated_at')

    id = serializers.ReadOnlyField(source='skill_id')
    skillset_id = serializers.ReadOnlyField(source='skill.skillset_id')
    name = serializers.ReadOnlyField(source='skill.name')
    description = serializers.ReadOnlyField(source='skill.description')
    verified = serializers.ReadOnlyField(source='skill.verified')
    weight = serializers.IntegerField(required=False)
