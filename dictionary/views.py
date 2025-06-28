from word import models as MODELS_WORD
from word_meaning import models as MODELS_MEAN
from example import models as MODELS_EXAM
from user import models as MODELS_USER
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from word.serializers.GET import serializer as SR_WORD
from help.common.generic import ghelp

def home(request):
    html_path = 'dictionary/home.html'
    context = {
        'title': 'Home',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'passage': ghelp.nav_links(key='passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
    }
    return render(request, html_path, context=context)