from django.contrib import admin
from word import models as MODELS_WORD

admin.site.register([
    MODELS_WORD.ComplexityLevel,
    MODELS_WORD.Word,
    MODELS_WORD.UserWord
])