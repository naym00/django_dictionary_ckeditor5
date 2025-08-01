from settings.serializers.GET import serializer as SR_SETT
from django.contrib.auth.decorators import login_required
from settings import models as MODELS_SETT
from help.common.generic import ghelp
from django.http import JsonResponse
from rest_framework import status

def get_general_settings(request):
    serialize_data = {}
    response_status = status.HTTP_400_BAD_REQUEST
    settings = ghelp.get_general_settings(MODELS_SETT.Settings)
    if settings:
        serialize_data = SR_SETT.SettingsSerializer(settings, many=False).data
        response_status = status.HTTP_200_OK
    return JsonResponse({'data': serialize_data}, status=response_status)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_user_settings(request):
    serialize_data = {}
    response_status = status.HTTP_400_BAD_REQUEST
    user_settings = ghelp.get_user_settings(request.user)
    
    if user_settings:
        serialize_data = SR_SETT.UserSettingsSerializer(user_settings, many=False).data
        response_status = status.HTTP_200_OK
    return JsonResponse({'data': serialize_data}, status=response_status)
