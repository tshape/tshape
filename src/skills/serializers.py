from rest_framework import serializers

from skills.models import Skill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'description', 'verified', 'skillset_id')
        read_only_fields = ('id',)

    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    verified = serializers.BooleanField(required=False)
    # skillset_id = serializers.IntegerField(required=False)
