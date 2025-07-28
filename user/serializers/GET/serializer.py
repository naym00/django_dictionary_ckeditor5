from rest_framework import serializers
from user import models as MODELS_USER

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_USER.User
        fields = ['id', 'username', 'first_name', 'last_name']