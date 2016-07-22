from rest_framework import serializers

from skillsets.models import Skillset


class SkillsetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified', 'weight')
        read_only_fields = ('id',)


class SkillsetUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skillset
        fields = ('id', 'name', 'description', 'verified', 'weight')
        read_only_fields = ('id',)

    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    weight = serializers.IntegerField(required=False)
