from rest_framework import serializers

from profiles.models import Profile
from skills.serializers import SkillSerializer
from skillsets.serializers import SkillsetSerializer
from users.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    skills = SkillSerializer(many=True)
    skillsets = SkillsetSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'title',
                  'description', 'years_experience', 'skills', 'skillsets')
        read_only_fields = ('user')

    # def __init__(self, *args, **kwargs):
    #     print(self)
    #     print(self.__dict__)
    #     print(args)
    #     print(kwargs)
    #     self.user_id = self.user.id
