from rest_framework import serializers

from profiles.models import Profile
from skills.serializers import SkillSerializer
from skillsets.serializers import SkillsetSerializer
from users.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'user', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'skills', 'skillsets')
        read_only_fields = ('user_id', 'user')

    user_id = serializers.IntegerField()
    user = UserSerializer(many=False)
    skills = SkillSerializer(many=True)
    skillsets = SkillsetSerializer(many=True)

    def get_user_id(self, obj):
        print(self)
        print(obj.__dict__)
        return self.user.id


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user_id', 'user', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'skills', 'skillsets')
        read_only_fields = ('user_id', 'user')

    user_id = serializers.IntegerField(required=False)
    user = UserSerializer(many=False, required=False)
    skills = SkillSerializer(many=True, required=False)
    skillsets = SkillsetSerializer(many=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)

    def get_user_id(self, obj):
        return self.user.id
