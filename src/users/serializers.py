from rest_framework import serializers

from profiles.serializers import ProfileListSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_active',
                  'date_joined', 'profile')
        read_only_fields = ('id', 'date_joined', 'profile')

    profile = ProfileListSerializer(required=False)


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_active',
                  'date_joined', 'profile')
        read_only_fields = ('id', 'date_joined', 'profile')

    email = serializers.EmailField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    date_joined = serializers.DateTimeField(required=False)
    profile = ProfileListSerializer(required=False)
