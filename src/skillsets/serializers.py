from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
    weight = serializers.IntegerField(required=False)
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False)


class SkillsetNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified', 'weight',
                  'created_at', 'updated_at')
        read_only_fields = (
            'id', 'name', 'description', 'verified', 'weight',
            'created_at', 'updated_at')

    name = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False)
