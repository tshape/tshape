from rest_framework import serializers

from skills.models import Skill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'skillset_id')
        read_only_fields = ('id',)

    skillset_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)


class SkillUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'skillset_id')
        read_only_fields = ('id', 'skillset_id')

    skillset_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)


class SkillNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'skillset_id')
        read_only_fields = (
            'id', 'name', 'description', 'verified', 'skillset_id')

    skillset_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
