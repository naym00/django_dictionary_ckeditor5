from rest_framework import serializers
from settings import models as MODELS_SETT

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_SETT.Settings
        fields='__all__'
        read_only_fields = ['id']