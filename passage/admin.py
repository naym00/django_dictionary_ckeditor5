from django.contrib import admin
from passage import models as MODELS_PASS

admin.site.register([
    MODELS_PASS.Passage,
    MODELS_PASS.Userpassage
])