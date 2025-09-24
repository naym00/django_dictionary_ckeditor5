from django.contrib.auth.decorators import login_required
from word.serializers.GET import serializer as SR_WORD
from word_meaning.serializers.GET import serializer as SR_MEAN
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from passage import models as MODELS_PASS
from passage import forms as FORMS_PASS
from word import models as MODELS_WORD
from user import models as MODELS_USER
from help.common.generic import ghelp
from help.choice import choice as CHOICE
from django.http import JsonResponse
from django.template.loader import render_to_string
from passage.services import passage_service
import requests

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
                'settings': ghelp.nav_links(key='settings'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'passages': MODELS_PASS.UserPassage.objects.filter(user=request.user, hide_from_mine_profile=False).order_by('-id'),
        'preview_passages': ghelp.get_passages_to_display(MODELS_USER.UserFriend, MODELS_PASS.UserPassage, request.user),
        'audiences': CHOICE.AUDIENCE,
        'friends': ghelp.get_friends(MODELS_USER.UserFriend, request.user, id=False),
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
                'settings': ghelp.nav_links(key='settings'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'form': FORMS_PASS.CreatePassageForm(),
        'audiences': CHOICE.AUDIENCE,
        'friends': ghelp.get_friends(MODELS_USER.UserFriend, request.user, id=False)
    }
    if request.method == 'POST':
        form = FORMS_PASS.CreatePassageForm(request.POST)
        if form.is_valid():
            audience = request.POST.get('audience')
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            instance = MODELS_PASS.Passage.objects.create(title=title, content=content, added_by=request.user)
            
            user_passage = MODELS_PASS.UserPassage.objects.create(user=request.user, passage=instance, title=title, content=content, audience=audience)
            for user_id in request.POST.getlist('audience_users'):
                MODELS_PASS.UserPassageShareOnly.objects.create(user_passage=user_passage, user=MODELS_USER.User.objects.get(id=user_id))
            return redirect('get-passages')
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def refetch_passages(request):
    for passage in request.user.added_by_passage.all():
        MODELS_PASS.UserPassage.objects.create(user=request.user, passage=passage, title=passage.title, content=passage.content, audience='Public')
    return redirect('get-passages')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def remove_passages(request):
    request.user.user_passages.all().delete()
    return redirect('get-passages')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def edit_passage(request, user_passage_id=None):
    html_path = 'dictionary/passage/edit_passage.html'
    user_passage = MODELS_PASS.UserPassage.objects.get(id=user_passage_id)
    
    context = {
        'title': 'Edit Passage',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'settings': ghelp.nav_links(key='settings'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'passage': user_passage,
        'form': FORMS_PASS.CreatePassageForm(initial={
            'title': user_passage.title,
            'content': user_passage.content
        }),
        'audiences': CHOICE.AUDIENCE,
        'friends': ghelp.get_friends(MODELS_USER.UserFriend, request.user, id=False),
        'selected_friends': [share.user.id for share in user_passage.audience_user_passages.select_related('user')]
    }
    if request.method == 'POST':
        if user_passage.user == request.user:
            form = FORMS_PASS.CreatePassageForm(request.POST)
            if form.is_valid():
                user_passage.title=form.cleaned_data['title']
                user_passage.content=form.cleaned_data['content']
                user_passage.audience=request.POST.get('audience')
                user_passage.save()
                user_passage.audience_user_passages.all().delete()
                
                for user_id in request.POST.getlist('audience_users'):
                    MODELS_PASS.UserPassageShareOnly.objects.create(user_passage=user_passage, user=MODELS_USER.User.objects.get(id=user_id))
                
                return redirect('get-single-passage', user_passage_id=user_passage_id)
        else: return redirect('get-single-passage', user_passage_id=user_passage_id)
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def reset_passage(request, user_passage_id=None):
    user_passage = MODELS_PASS.UserPassage.objects.get(id=user_passage_id)
    if user_passage.user == request.user:
        user_passage.title=user_passage.passage.title
        user_passage.content=user_passage.passage.content
        user_passage.save()
    return redirect('get-single-passage', user_passage_id=user_passage_id)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_single_passage(request, user_passage_id=None):
    html_path = 'dictionary/passage/single_passage.html'
    user_passage = MODELS_PASS.UserPassage.objects.get(id=user_passage_id)
    context = {
        'title': 'Single Passage',
        'user': request.user,
        'nav_links': {
            'auth': {
                'home': ghelp.nav_links(key='home', user=request.user),
                'view_passage': ghelp.nav_links(key='view_passage'),
                'add_passage': ghelp.nav_links(key='add_passage'),
                'words': ghelp.nav_links(key='words'),
                'settings': ghelp.nav_links(key='settings'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'user_settings': ghelp.get_user_settings(request.user),
        'levels': SR_WORD.ComplexityLevelSerializer(MODELS_WORD.ComplexityLevel.objects.all().order_by('difficulty_level'), many=True).data,
        'passage': user_passage,
        'notes': passage_service.get_user_passage_notes(request, user_passage),
        'form': FORMS_PASS.CreatePassageNote(initial={
            'note': user_passage.note
        })
    }
    if request.method == 'POST':
        if user_passage.user == request.user:
            form = FORMS_PASS.CreatePassageNote(request.POST)
            if form.is_valid():
                user_passage.note=form.cleaned_data['note']
                user_passage.save()
                return redirect('get-single-passage', user_passage_id=user_passage_id)
    
    if request.headers.get('X-Request-Type') == 'Word-Complexity-Level':
        page_obj = Paginator(
                passage_service.get_user_passage_words(request, user_passage),
                int(request.GET.get('page_size', 10))
            ).get_page(int(request.GET.get('page', 1)))
        return JsonResponse({
                'data': {
                    'words': passage_service.serialized_user_passage_words(page_obj.object_list),
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'page_number': page_obj.number,
                    'last_page': page_obj.paginator.num_pages
                },
                'levels': SR_WORD.ComplexityLevelSerializer(MODELS_WORD.ComplexityLevel.objects.all().order_by('difficulty_level'), many=True).data
            }, status=200)
    elif request.headers.get('X-Request-Type') == 'Selected-Word-Meaning':
        meanings = []
        is_own_source = True
        word_text = request.GET.get('word')
        if word_text:
            word = MODELS_WORD.Word.objects.filter(text=word_text.strip().capitalize())
            if word.exists(): meanings = SR_MEAN.WordMeaningSerializer(word.first().meanings.all(), many=True).data
            else:
                response = None
                try: response = requests.get(f'https://lingva.ml/api/v1/en/bn/{word_text.strip().lower()}')
                except: pass
                if response != None:
                    if response.status_code:
                        meanings = [{'text': response.json()['translation']}]
                        is_own_source = False
                else:
                    meanings = [{'text': 'দুঃখিত, আপাতত ইন্টারনেট সংযোগ নেই।'}]
                    is_own_source = False
        return JsonResponse({'meanings': meanings, 'is_own_source': is_own_source})
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def remove_passage_from_my_list(request, user_passage_id=None):
    MODELS_PASS.UserPassage.objects.get(id=user_passage_id).delete()
    return redirect('get-passages')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_passage_to_your_list(request, passage_id=None):
    if request.method == 'POST':
        audience = request.POST.get('audience')
        passage=MODELS_PASS.Passage.objects.get(id=passage_id)
        user_passage = MODELS_PASS.UserPassage.objects.create(user=request.user, passage=passage, title=passage.title, content=passage.content, audience=audience)
        for user_id in request.POST.getlist('audience_users'):
            MODELS_PASS.UserPassageShareOnly.objects.create(user_passage=user_passage, user=MODELS_USER.User.objects.get(id=user_id))
    return redirect('get-passages')