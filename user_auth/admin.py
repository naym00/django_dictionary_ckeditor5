from django.contrib import admin
from user_auth import models as MODELS_AUTH

admin.site.register([
    MODELS_AUTH.Forgotpassword
])