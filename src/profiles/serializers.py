from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'skillset_ids',
                  'skill_ids', 'created_at', 'updated_at')
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'created_at',
                  'updated_at')
        read_only_fields = ('user_id', 'created_at', 'updated_at')

    user_id = serializers.PrimaryKeyRelatedField(
        many=False, read_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)
