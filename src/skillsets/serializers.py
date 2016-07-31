from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from skills.serializers import SkillNestedSerializer
from skillsets.models import Skillset


class SkillsetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified',
                  'weight', 'skills')
        read_only_fields = ('id', 'skills')

    name = serializers.CharField(validators=[
        UniqueValidator(queryset=Skillset.objects.all())])
    description = serializers.CharField(required=False)


class SkillsetUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified', 'weight', 'skills')
        read_only_fields = ('id', 'skills')

    skills = SkillNestedSerializer(many=True, required=False, read_only=True)
    name = serializers.CharField(required=False, validators=[
        UniqueValidator(queryset=Skillset.objects.all())])
    description = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False)


class SkillsetNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified', 'weight')
        read_only_fields = (
            'id', 'name', 'description', 'verified', 'weight')

    name = serializers.CharField(required=False, validators=[
        UniqueValidator(queryset=Skillset.objects.all())])
    description = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False)
