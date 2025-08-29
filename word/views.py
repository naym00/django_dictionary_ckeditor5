from django.contrib.auth.decorators import login_required
from word.serializers.GET import serializer as SR_WORD
from word_meaning import models as MODELS_MEAN
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from example import models as MODELS_EXAM
from passage import models as MODELS_PASS
from word import models as MODELS_WORD
from help.common.generic import ghelp
from django.http import JsonResponse
from rest_framework import status


@login_required(login_url=ghelp.nav_links(key='login')['link'])
def get_words(request):
    html_path = 'dictionary/word/get-words.html'
    
    filter_dict = ghelp.prepare_word_filter_dict(
        request.user,
        {'attribute': 'level__difficulty_level', 'value': request.GET.get('complexity', '0')},
        new={'attribute': 'created_at__gte', 'value': request.GET.get('keyword')},
        search={'attribute': 'word__text__icontains', 'value': request.GET.get('search')},
        meaning_search={'attribute': 'word__meanings__text__icontains', 'value': request.GET.get('meaning_search')}
    )
    serialized_levels = SR_WORD.ComplexityLevelSerializer(MODELS_WORD.ComplexityLevel.objects.all().order_by('difficulty_level'), many=True).data
    context = {
        'title': 'Words',
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
            }, status=status.HTTP_200_OK)
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_word(request):
    text = request.GET.get('text')
    if text:
        text = ghelp.prepare_text(text)
        pronunciation = request.GET.get('pronunciation')
        example = request.GET.get('example')
        difficult_level = int(request.GET.get('difficult_level'))
        
        word_instance = MODELS_WORD.Word.objects.filter(text=text)
        if word_instance.exists(): word_instance = word_instance.first()
        else:
            word_instance = MODELS_WORD.Word.objects.create(
                text=text,
                pronunciation=pronunciation.strip() if pronunciation != '' else None,
                added_by=request.user
            )
        if example != '': MODELS_EXAM.Example.objects.create(sentence=ghelp.prepare_text(example), word=word_instance, added_by=request.user)
        
        for meaning in ghelp.split_word_meanings(request.GET.get('meanings')):
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
    return JsonResponse({'success': True}, status=status.HTTP_200_OK)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def edit_word(request, id=None):
    if request.method == 'POST':
        form_tobe_edited = {}
        text = request.POST.get('text')
        if text:
            text = ghelp.prepare_text(text)
            if not MODELS_WORD.Word.objects.filter(text=text).exists(): form_tobe_edited.update({'text': text})
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
            MODELS_WORD.UserWord.objects.filter(id=id).update(level=MODELS_WORD.ComplexityLevel.objects.get(id=difficult_level), right_prediction=0, wrong_prediction=0)
    return redirect('get-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def increment_right_prediction(request, id=None):
    is_complexity_level_changed = False
    user_word = MODELS_WORD.UserWord.objects.get(id=id)
    right_prediction = user_word.right_prediction+1
    
    level = MODELS_WORD.ComplexityLevel.objects.filter(is_complexity_level=True, difficulty_level__lt=user_word.level.difficulty_level).order_by('difficulty_level').last()
    if level:
        user_settings = ghelp.get_user_settings(request.user)
        if right_prediction >= user_settings.right_prediction_to_change_complexity_level:
            user_word.level=level
            right_prediction = 0
            is_complexity_level_changed = True
    user_word.right_prediction=right_prediction
    user_word.save()
    return JsonResponse({'success': True, 'is_complexity_level_changed': is_complexity_level_changed}, status=status.HTTP_200_OK)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def increment_wrong_prediction(request, id=None):
    is_complexity_level_changed = False
    user_word = MODELS_WORD.UserWord.objects.get(id=id)
    wrong_prediction = user_word.wrong_prediction+1
    
    level = MODELS_WORD.ComplexityLevel.objects.filter(is_complexity_level=True, difficulty_level__gt=user_word.level.difficulty_level).order_by('difficulty_level').first()
    if level:
        user_settings = ghelp.get_user_settings(request.user)
        if wrong_prediction >= user_settings.wrong_prediction_to_change_complexity_level:
            user_word.level=level
            wrong_prediction = 0
            is_complexity_level_changed = True
    user_word.wrong_prediction=wrong_prediction
    user_word.save()
    return JsonResponse({'success': True, 'is_complexity_level_changed': is_complexity_level_changed}, status=status.HTTP_200_OK)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_word_from_passage(request, user_passage_id=None):
    text = request.GET.get('text')
    if text:
        text = ghelp.prepare_text(text)
        user_passage = MODELS_PASS.UserPassage.objects.get(id=user_passage_id)
        difficult_level = int(request.GET.get('difficult_level'))
        
        
        word_instance = MODELS_WORD.Word.objects.filter(text=text)
        if word_instance.exists(): word_instance = word_instance.first()
        else: word_instance = MODELS_WORD.Word.objects.create(text=text, added_by=request.user)
            
        for meaning in ghelp.split_word_meanings(request.GET.get('meanings')):
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
    return JsonResponse({'success': True}, status=status.HTTP_200_OK)