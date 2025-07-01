from django.contrib.auth.decorators import login_required
from passage.serializers.GET import serializer as SR_PASS
from word.serializers.GET import serializer as SR_WORD
from django.shortcuts import render, redirect
from passage import models as MODELS_PASS
from passage import forms as FORMS_PASS
from word import models as MODELS_WORD
from user import models as MODELS_USER
from help.common.generic import ghelp

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_passages(request):
    html_path = 'dictionary/passage/get_passage.html'
    context = {
        'title': 'Passage',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'passages': SR_PASS.Passageserializer(MODELS_PASS.Passage.objects.filter(passage_users__user=request.user).order_by('-id'), many=True).data,
        'friends_passages': MODELS_PASS.Userpassage.objects.filter(
                            user__in=list(MODELS_USER.Userfriend.objects.filter(user=request.user).values_list('friend', flat=True)) + list(MODELS_USER.Userfriend.objects.filter(friend=request.user).values_list('user', flat=True))
                        ).select_related('passage', 'user')
    }
    return render(request, html_path, context=context)


@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_passage(request):
    html_path = 'dictionary/passage/add_passage.html'
    context = {
        'title': 'Add Passage',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'form': FORMS_PASS.CreatePassageForm()
    }
    if request.method == 'POST':
        form = FORMS_PASS.CreatePassageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            instance = MODELS_PASS.Passage.objects.create(title=title, content=content, added_by=request.user)
            
            MODELS_PASS.Userpassage.objects.create(user=request.user, passage=instance)
            return redirect('get-passages')
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_passage_using_id(request, passageid=None):
    html_path = 'dictionary/passage/passage_using_id.html'
    passage = MODELS_PASS.Passage.objects.get(id=passageid)
    
    # userwords = MODELS_WORD.Userword.objects.filter(
    #     user=request.user,  # Filter for logged-in user
    #     word__word_passages__passage_id=passageid  # Filter for words in the passage
    # ).distinct().order_by('-id')
    
    context = {
        'title': 'Single Passage',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'word_details': ghelp.nav_links(key='word_details'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data,
        'passage': passage,
        'words': SR_WORD.Userwordserializer(
            request.user.user_words.filter(
                word__word_passages__passage_id=passageid
            ).distinct().order_by('-id'),
            many=True
        ).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def remove_passage_from_my_list(request, passageid=None):
    request.user.user_passages.filter(passage=passageid).delete()
    return redirect('get-passages')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_passage_to_your_list(request, passageid=None):
    MODELS_PASS.Userpassage.objects.create(user=request.user, passage=MODELS_PASS.Passage.objects.get(id=passageid))
    return redirect('get-passages')