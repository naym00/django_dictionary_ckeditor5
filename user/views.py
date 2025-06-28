from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user import models as MODELS_USER
from settings import models as MODELS_SETT
from help.common.generic import ghelp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def unique_username(request, username=None):
    existance_of_username = False
    if username != None:
        existance_of_username = MODELS_USER.User.objects.filter(username=username).exists()
    return Response({'is_exist': existance_of_username}, status=status.HTTP_200_OK)