from rest_framework import serializers
from word_meaning import models as MODELS_MEAN
from user.serializers.GET.serializer import UserSerializer

class WordMeaningSerializer(serializers.ModelSerializer):
    added_by = UserSerializer(many=False)
    class Meta:
        model = MODELS_MEAN.WordMeaning
        fields='__all__'
        read_only_fields = ['id', 'created_at']