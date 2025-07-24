from rest_framework import serializers
from word import models as MODELS_WORD
from word_meaning.serializers.GET.serializer import WordMeaningSerializer
from example.serializers.GET.serializer import ExampleSerializer

class ComplexityLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_WORD.ComplexityLevel
        fields='__all__'
        read_only_fields = ['id', 'created_at']

class WordSerializer(serializers.ModelSerializer):
    meanings = WordMeaningSerializer(many=True)
    examples = ExampleSerializer(many=True)
    
    class Meta:
        model = MODELS_WORD.Word
        fields='__all__'
        read_only_fields = ['id', 'created_at']

class UserWordSerializer(serializers.ModelSerializer):
    word = WordSerializer(many=False)
    level = ComplexityLevelSerializer(many=False)
    date_time = serializers.SerializerMethodField('format_datetime')

    def format_datetime(self, instance):
        return instance.created_at
    class Meta:
        model = MODELS_WORD.UserWord
        fields='__all__'
        read_only_fields = ['id', 'created_at']