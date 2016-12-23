from rest_framework import serializers

from profiles.serializers import ProfileListSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'title',
                  'years_experience', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')

    profile = ProfileListSerializer(required=False)


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'title',
                  'years_experience', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')

    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    years_experience = serializers.IntegerField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    date_joined = serializers.DateTimeField(required=False)
    profile = ProfileListSerializer(required=False)
