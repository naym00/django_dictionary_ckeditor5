from rest_framework import serializers
from passage import models as MODELS_PASS

class PassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_PASS.Passage
        fields='__all__'
        read_only_fields = ['id', 'created_at']