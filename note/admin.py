from django.contrib import admin
from note import models as MODELS_NOTE

admin.site.register([
    MODELS_NOTE.Note,
    MODELS_NOTE.UserNote
])