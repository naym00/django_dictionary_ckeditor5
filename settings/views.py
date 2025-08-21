from settings.serializers.GET import serializer as SR_SETT
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from settings import models as MODELS_SETT
from word import models as MODELS_WORD
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
    html_path = 'dictionary/settings/get-user-settings.html'
    user_settings = ghelp.get_user_settings(request.user)
    general_Settings = ghelp.get_general_settings(MODELS_SETT.Settings)
    context = {
        'title': 'Settings',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'data': {
            'is_admin': True if request.user.user_type == 'Admin' else False,
            'complexitys': MODELS_WORD.ComplexityLevel.objects.all().order_by('difficulty_level'),
            'general_Settings': general_Settings,
            'user_settings': user_settings,
        }
    }
    if request.method == 'POST':
        complexity_texts = request.POST.getlist('complexity_text')
        complexity_difficulty_levels = request.POST.getlist('complexity_difficulty_level')
        print(complexity_texts)
        print(complexity_difficulty_levels)
        
        otp_validation_minutes = request.POST.get('otp_validation_minutes')
        new_word_day_duration = request.POST.get('new_word_day_duration')
        words_per_page = request.POST.get('words_per_page')
        
        if otp_validation_minutes: general_Settings.otp_validation_minutes = otp_validation_minutes
        general_Settings.save()
        
        if new_word_day_duration: user_settings.new_word_day_duration = new_word_day_duration
        if words_per_page: user_settings.words_per_page = words_per_page
        user_settings.save()
        return redirect('get-user-settings')
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_user_settings_json(request):
    serialize_data = {}
    response_status = status.HTTP_400_BAD_REQUEST
    user_settings = ghelp.get_user_settings(request.user)
    
    if user_settings:
        serialize_data = SR_SETT.UserSettingsSerializer(user_settings, many=False).data
        response_status = status.HTTP_200_OK
    return JsonResponse({'data': serialize_data}, status=response_status)
