from django.contrib import admin
from passage import models as MODELS_PASS

admin.site.register([
    MODELS_PASS.IeltsBook,
    MODELS_PASS.Passage,
    MODELS_PASS.PassageWord,
    MODELS_PASS.PassageNote,
    MODELS_PASS.UserPassage,
    MODELS_PASS.UserPassageShareOnly
])