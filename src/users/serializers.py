from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_active', 'date_joined',
                  'first_name', 'last_name')
        read_only_fields = ('id', 'date_joined')


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_active', 'date_joined',
                  'first_name', 'last_name')
        read_only_fields = ('id', 'date_joined')

    email = serializers.EmailField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    date_joined = serializers.DateTimeField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
