from rest_framework import serializers
from passage import models as MODELS_PASS

class Passageserializer(serializers.ModelSerializer):
    class Meta:
        model = MODELS_PASS.Passage
        fields='__all__'
        
# class Userpassageserializer(serializers.ModelSerializer):
#     class Meta:
#         model = MODELS_PASS.Userpassage
#         fields='__all__'