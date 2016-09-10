from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from profiles.models import ProfileSkillset
from skillsets.models import Skillset


class SkillsetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified',
                  'weight', 'skill_ids', 'created_at', 'updated_at')
        read_only_fields = ('id', 'skill_ids', 'created_at', 'updated_at')

    name = serializers.CharField(validators=[
        UniqueValidator(queryset=Skillset.objects.all())])
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False)


class SkillsetUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified', 'weight',
                  'skill_ids', 'created_at', 'updated_at')
        read_only_fields = ('id', 'skill_ids', 'created_at', 'updated_at')

    name = serializers.CharField(required=False, validators=[
        UniqueValidator(queryset=Skillset.objects.all())])
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False, allow_null=True)
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False)


class ProfileSkillsetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileSkillset
        fields = ('id', 'name', 'description', 'verified', 'profile_weight',
                  'created_at', 'updated_at')
        read_only_fields = (
            'id', 'name', 'description', 'verified',
            'created_at', 'updated_at')

    id = serializers.ReadOnlyField(source='skillset_id')
    name = serializers.ReadOnlyField(source='skillset.name')
    description = serializers.ReadOnlyField(source='skillset.description')
    verified = serializers.ReadOnlyField(source='skillset.verified')
    profile_weight = serializers.IntegerField(required=False)
