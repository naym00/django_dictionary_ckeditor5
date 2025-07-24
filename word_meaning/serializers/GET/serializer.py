from rest_framework import serializers
from word_meaning import models as MODELS_MEAN

class WordMeaningSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_MEAN.WordMeaning
        fields='__all__'
        read_only_fields = ['id', 'created_at']