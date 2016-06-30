from rest_framework import serializers

from tshape.models import BaseModel


class BaseModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseModel
        fields = ('created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
