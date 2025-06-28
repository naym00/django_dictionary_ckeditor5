from django.contrib.auth.decorators import login_required
from word.serializers.GET import serializer as SR_WORD
from word_meaning import models as MODELS_MEAN
from django.shortcuts import render, redirect
from example import models as MODELS_EXAM
from word import models as MODELS_WORD
from help.common.generic import ghelp

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def words(request):
    html_path = 'dictionary/word/words.html'
    context = {
        'title': 'Words',
        'user': request.user,
        'words': SR_WORD.Wordserializer(MODELS_WORD.Word.objects.all().order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def new_words(request):
    html_path = 'dictionary/word/new_words.html'
    context = {
        'title': 'New Words',
        'user': request.user,
        'words': SR_WORD.Wordserializer(MODELS_WORD.Word.objects.filter(created_at__gte=ghelp.n_days_back_datetime(n_days=10, zone=ghelp.dhaka_timezone)).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def easy_words(request):
    html_path = 'dictionary/word/easy_words.html'
    context = {
        'title': 'Easy Words',
        'user': request.user,
        'words': SR_WORD.Wordserializer(MODELS_WORD.Word.objects.filter(level__difficulty_level=1).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def medium_words(request):
    html_path = 'dictionary/word/medium_words.html'
    context = {
        'title': 'Medium Words',
        'user': request.user,
        'words': SR_WORD.Wordserializer(MODELS_WORD.Word.objects.filter(level__difficulty_level=2).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def hard_words(request):
    html_path = 'dictionary/word/hard_words.html'
    context = {
        'title': 'Hard Words',
        'user': request.user,
        'words': SR_WORD.Wordserializer(MODELS_WORD.Word.objects.filter(level__difficulty_level=3).order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def word_details(request):
    html_path = 'dictionary/word/word_details.html'
    context = {
        'title': 'Words',
        'user': request.user,
        'words': SR_WORD.Wordserializer(MODELS_WORD.Word.objects.all().order_by('-id'), many=True).data,
        'level': SR_WORD.Complexitylevelserializer(MODELS_WORD.Complexitylevel.objects.all(), many=True).data
    }
    return render(request, html_path, context=context)

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def add_word(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        pronunciation = request.POST.get('pronunciation')
        meaning = request.POST.get('meaning')
        example = request.POST.get('example')
        difficult_level = request.POST.get('difficult_level')
        
        word_instance = MODELS_WORD.Word.objects.create(
            user=request.user,
            text=word.strip().capitalize(),
            pronunciation= pronunciation if pronunciation != '' else None,
            level=MODELS_WORD.Complexitylevel.objects.get(id=difficult_level)
        )
        if example != '': MODELS_EXAM.Example.objects.create(sentence=example, word=word_instance)
        MODELS_MEAN.Wordmeaning.objects.create(text=meaning, word=word_instance)
        
    return redirect('preview-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def edit_word(request, id=None):
    if request.method == 'POST':
        form_tobe_edited = {}
        text = request.POST.get('text')
        if text: form_tobe_edited.update({'text': text.strip().capitalize()})
        pronunciation = request.POST.get('pronunciation')
        if pronunciation: form_tobe_edited.update({'pronunciation': pronunciation})
        difficult_level = request.POST.get('difficult_level')
        if difficult_level: form_tobe_edited.update({'level': MODELS_WORD.Complexitylevel.objects.get(id=difficult_level)})
        
        MODELS_WORD.Word.objects.filter(id=id).update(**form_tobe_edited)
    return redirect('preview-words')

@login_required(login_url=ghelp.nav_links(key='login')['link'])
def delete_word(request, id=None):
    MODELS_WORD.Word.objects.get(id=id).delete()
    return redirect('preview-words')