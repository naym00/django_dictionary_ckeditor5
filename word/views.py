from django.contrib.auth.decorators import login_required
from word.serializers.GET import serializer as SR_WORD
from word_meaning import models as MODELS_MEAN
from django.shortcuts import render, redirect
from example import models as MODELS_EXAM
from word import models as MODELS_WORD
from passage import models as MODELS_PASS
from settings import models as MODELS_SETT
from django.core.paginator import Paginator
from help.common.generic import ghelp
from django.http import JsonResponse
import re

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_words(request):
    html_path = 'dictionary/word/get-words.html'

    filter_dict = ghelp.prepare_word_filter_dict(MODELS_SETT.Settings, request.GET.get('complexity', '0'), request.GET.get('keyword'))
    serialized_levels = SR_WORD.ComplexityLevelSerializer(MODELS_WORD.ComplexityLevel.objects.all(), many=True).data
    context = {
        'title': 'Words',
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
        'levels': serialized_levels
    }
    if request.headers.get('X-Request-Type') == 'Words-Level':
        page_obj = Paginator(
                request.user.user_words.filter(**filter_dict).order_by('-id'),
                int(request.GET.get('page_size', 10))
            ).get_page(int(request.GET.get('page', 1)))
        return JsonResponse({
                'data': {
                    'words': SR_WORD.UserWordSerializer(page_obj.object_list, many=True).data,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'page_number': page_obj.number,
                    'last_page': page_obj.paginator.num_pages
                },
                'levels': serialized_levels
            }, status=200)
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_word(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        pronunciation = request.POST.get('pronunciation')
        meanings = re.split('[|.,;]', request.POST.get('meaning'))
        example = request.POST.get('example')
        difficult_level = int(request.POST.get('difficult_level'))
        
        word_instance = MODELS_WORD.Word.objects.filter(text=text.strip().capitalize())
        if word_instance.exists(): word_instance = word_instance.first()
        else:
            word_instance = MODELS_WORD.Word.objects.create(
                text=text.strip().capitalize(),
                pronunciation= pronunciation.strip() if pronunciation != '' else None,
                added_by=request.user
            )
        if example != '': MODELS_EXAM.Example.objects.create(sentence=example.strip().capitalize(), word=word_instance, added_by=request.user)
        # MODELS_MEAN.WordMeaning.objects.create(text=meaning, word=word_instance, added_by=request.user)
        for meaning in meanings:
            meaning = meaning.strip()
            if meaning:
                word_meaning = word_instance.meanings.filter(text=meaning)
                if not word_meaning.exists():
                    MODELS_MEAN.WordMeaning.objects.create(text=meaning, word=word_instance, added_by=request.user)

        user_word = request.user.user_words.filter(word=word_instance)
        if user_word.exists():
            if user_word.first().level.id != difficult_level:
                user_word.update(level=MODELS_WORD.ComplexityLevel.objects.get(id=difficult_level))
        else:
            MODELS_WORD.UserWord.objects.create(
                user=request.user,
                word=word_instance,
                level=MODELS_WORD.ComplexityLevel.objects.get(id=difficult_level)
            )
    return redirect('get-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def edit_word(request, id=None):
    if request.method == 'POST':
        form_tobe_edited = {}
        text = request.POST.get('text')
        if text:
            text = text.strip().capitalize()
            if not MODELS_WORD.Word.objects.filter(text=text).exists():
                form_tobe_edited.update({'text': text})
        pronunciation = request.POST.get('pronunciation')
        if pronunciation: form_tobe_edited.update({'pronunciation': pronunciation})
        
        if form_tobe_edited:
            MODELS_WORD.Word.objects.filter(id=id).update(**form_tobe_edited)
    return redirect('get-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def delete_word(request, id=None):
    MODELS_WORD.Word.objects.get(id=id).delete()
    return redirect('get-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def edit_word_complexity_level(request, id=None):
    if request.method == 'POST':
        difficult_level = request.POST.get('difficult_level')
        if difficult_level:
            MODELS_WORD.UserWord.objects.filter(id=id).update(level=MODELS_WORD.ComplexityLevel.objects.get(id=difficult_level))
    return redirect('get-words')


@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_word_from_passage(request, user_passage_id=None):
    if request.method == 'POST':
        user_passage = MODELS_PASS.UserPassage.objects.get(id=user_passage_id)
        
        text = request.POST.get('text')
        meanings = re.split('[|.,;]', request.POST.get('meaning'))
        difficult_level = int(request.POST.get('difficult_level'))
        
        
        word_instance = MODELS_WORD.Word.objects.filter(text=text.strip().capitalize())
        if word_instance.exists(): word_instance = word_instance.first()
        else:
            word_instance = MODELS_WORD.Word.objects.create(
                text=text.strip().capitalize(),
                added_by=request.user
            )
            
        for meaning in meanings:
            meaning = meaning.strip()
            if meaning:
                word_meaning = word_instance.meanings.filter(text=meaning)
                if not word_meaning.exists():
                    MODELS_MEAN.WordMeaning.objects.create(text=meaning, word=word_instance, added_by=request.user)
        
        userword = request.user.user_words.filter(word=word_instance)
        if not userword.exists():
            MODELS_WORD.UserWord.objects.create(user=request.user, word=word_instance, level=MODELS_WORD.ComplexityLevel.objects.get(id=difficult_level))
        else:
            if userword.first().level.id != difficult_level:
                userword.update(level=MODELS_WORD.ComplexityLevel.objects.get(id=difficult_level))
        
        passageword = word_instance.word_passages.filter(passage=user_passage.passage.id)
        if not passageword.exists():
            MODELS_PASS.PassageWord.objects.create(word=word_instance, passage=MODELS_PASS.Passage.objects.get(id=user_passage.passage.id))
    return redirect('get-passage-using-id', user_passage_id=user_passage_id)