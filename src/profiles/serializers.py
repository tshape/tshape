from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'skillset_ids',
                  'skill_ids', 'created_at', 'updated_at')
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'created_at', 'updated_at')
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
