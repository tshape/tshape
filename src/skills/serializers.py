from rest_framework import serializers

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
