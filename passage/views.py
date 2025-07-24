from django.contrib.auth.decorators import login_required
from word.serializers.GET import serializer as SR_WORD
from django.shortcuts import render, redirect
from passage import models as MODELS_PASS
from passage import forms as FORMS_PASS
from word import models as MODELS_WORD
from user import models as MODELS_USER
from help.common.generic import ghelp
from help.choice import choice as CHOICE

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
        'passages': MODELS_PASS.UserPassage.objects.filter(user=request.user).order_by('-id'),
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
                'word_details': ghelp.nav_links(key='word_details'),
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
                'word_details': ghelp.nav_links(key='word_details'),
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
                
                return redirect('get-passage-using-id', user_passage_id=user_passage_id)
        else: return redirect('get-passage-using-id', user_passage_id=user_passage_id)
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def reset_passage(request, user_passage_id=None):
    user_passage = MODELS_PASS.UserPassage.objects.get(id=user_passage_id)
    if user_passage.user == request.user:
        user_passage.title=user_passage.passage.title
        user_passage.content=user_passage.passage.content
        user_passage.save()
    return redirect('get-passage-using-id', user_passage_id=user_passage_id)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_passage_using_id(request, user_passage_id=None):
    html_path = 'dictionary/passage/passage_using_id.html'
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
                'word_details': ghelp.nav_links(key='word_details'),
                'logout': ghelp.nav_links(key='logout')
            },
            'unauth': {
                'home': ghelp.nav_links(key='home'),
                'login': ghelp.nav_links(key='login'),
                'register': ghelp.nav_links(key='register'),
            }
        },
        'level': SR_WORD.ComplexityLevelSerializer(MODELS_WORD.ComplexityLevel.objects.all(), many=True).data,
        'passage': user_passage,
        'form': FORMS_PASS.CreatePassageNote(initial={
            'note': user_passage.note
        }),
        'words': SR_WORD.UserWordSerializer(
            request.user.user_words.filter(
                word__word_passages__passage_id=user_passage.passage.id
            ).distinct().order_by('-id'),
            many=True
        ).data
    }
    if request.method == 'POST':
        if user_passage.user == request.user:
            form = FORMS_PASS.CreatePassageNote(request.POST)
            if form.is_valid():
                user_passage.note=form.cleaned_data['note']
                user_passage.save()
                return redirect('get-passage-using-id', user_passage_id=user_passage_id)
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