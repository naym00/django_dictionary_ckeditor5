from django.contrib.auth.decorators import login_required
from word.serializers.GET import serializer as SR_WORD
from word_meaning import models as MODELS_MEAN
from django.shortcuts import render, redirect
from example import models as MODELS_EXAM
from word import models as MODELS_WORD
from settings import models as MODELS_SETT
from help.common.generic import ghelp

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def words(request):
    html_path = 'dictionary/word/words.html'
    context = {
        'title': 'Words',
        'user': request.user,
        'words': SR_WORD.Userwordserializer(request.user.user_words.all().order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def new_words(request):
    settings = ghelp.get_settings(MODELS_SETT.Settings)
    if settings:
        html_path = 'dictionary/word/new_words.html'
        context = {
            'title': 'New Words',
            'user': request.user,
            'words': SR_WORD.Userwordserializer(
                request.user.user_words.filter(
                    created_at__gte=ghelp.n_days_back_datetime(
                        n_days=settings.new_word_day_duration,
                        zone=ghelp.dhaka_timezone
                    )
                ).order_by('-id'),
                many=True
            ).data,
            'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
        }
        return render(request, html_path, context=context)
    return redirect('preview-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def easy_words(request):
    html_path = 'dictionary/word/easy_words.html'
    context = {
        'title': 'Easy Words',
        'user': request.user,
        'words': SR_WORD.Userwordserializer(request.user.user_words.filter(level__difficulty_level=1).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def medium_words(request):
    html_path = 'dictionary/word/medium_words.html'
    context = {
        'title': 'Medium Words',
        'user': request.user,
        'words': SR_WORD.Userwordserializer(request.user.user_words.filter(level__difficulty_level=2).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def hard_words(request):
    html_path = 'dictionary/word/hard_words.html'
    context = {
        'title': 'Hard Words',
        'user': request.user,
        'words': SR_WORD.Userwordserializer(request.user.user_words.filter(level__difficulty_level=3).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def word_details(request):
    html_path = 'dictionary/word/word_details.html'
    context = {
        'title': 'Words',
        'user': request.user,
        'words': SR_WORD.Userwordserializer(request.user.user_words.all().order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_word(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        pronunciation = request.POST.get('pronunciation')
        meaning = request.POST.get('meaning')
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
        if example != '': MODELS_EXAM.Example.objects.create(sentence=example.strip().capitalize(), word=word_instance)
        MODELS_MEAN.Wordmeaning.objects.create(text=meaning, word=word_instance)

        user_word = request.user.user_words.filter(word=word_instance)
        if user_word.exists():
            if user_word.first().level.id != difficult_level:
                user_word.update(level=MODELS_WORD.Complexitylevel.objects.get(id=difficult_level))
        else:
            MODELS_WORD.Userword.objects.create(
                user=request.user,
                word=word_instance,
                level=MODELS_WORD.Complexitylevel.objects.get(id=difficult_level)
            )
    return redirect('preview-words')

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
    return redirect('preview-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def delete_word(request, id=None):
    MODELS_WORD.Word.objects.get(id=id).delete()
    return redirect('preview-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def edit_word_complexity_level(request, id=None):
    if request.method == 'POST':
        difficult_level = request.POST.get('difficult_level')
        if difficult_level:
            MODELS_WORD.Userword.objects.filter(id=id).update(level=MODELS_WORD.Complexitylevel.objects.get(id=difficult_level))
    return redirect('preview-words')