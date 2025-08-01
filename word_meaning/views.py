from word import models as MODELS_WORD
from word_meaning import models as MODELS_MEAN
from django.shortcuts import redirect
from help.common.generic import ghelp

def add_word_meaning(request, word_id=None):
    if request.method == 'POST':
        word_instance = MODELS_WORD.Word.objects.get(id=word_id)
        for meaning in ghelp.split_word_meanings(request.POST.get('meanings')):
            meaning = meaning.strip()
            if meaning:
                word_meaning = word_instance.meanings.filter(text=meaning)
                if not word_meaning.exists():
                    MODELS_MEAN.WordMeaning.objects.create(text=meaning, word=word_instance, added_by=request.user)
    return redirect('get-words')

def edit_word_meaning(request, id=None):
    if request.method == 'POST':
        meaning = request.POST.get('meaning')
        MODELS_MEAN.WordMeaning.objects.filter(id=id).update(text=meaning)
    return redirect('get-words')
    
def delete_word_meaning(request, id=None):
    MODELS_MEAN.WordMeaning.objects.get(id=id).delete()
    return redirect('get-words')