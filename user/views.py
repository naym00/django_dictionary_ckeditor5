from django.contrib.auth.decorators import login_required
from user import models as MODELS_USER
from help.common.generic import ghelp
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def send_friend_request(request, requested_to_id=None):
    MODELS_USER.Friendrequest.objects.create(user=request.user, requested_to=MODELS_USER.User.objects.get(id=requested_to_id))
    return redirect('home')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def accept_friend_request(request, user_id=None):
    friend_request = request.user.requested_to_users.filter(user=user_id)
    MODELS_USER.Userfriend.objects.create(user=request.user, friend=friend_request.first().user)
    friend_request.delete()
    return redirect('home')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def delete_friend_request(request, user_id=None):
    friend_request = request.user.requested_to_users.filter(user=user_id)
    friend_request.delete()
    return redirect('home')

@api_view(['GET'])
def unique_username(request, username=None):
    existance_of_username = False
    if username != None:
        existance_of_username = MODELS_USER.User.objects.filter(username=username).exists()
    return Response({'is_exist': existance_of_username}, status=status.HTTP_200_OK)