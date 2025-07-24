from rest_framework import serializers
from example import models as MODELS_EXAM

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_EXAM.Example
        fields='__all__'
        read_only_fields = ['id', 'created_at']