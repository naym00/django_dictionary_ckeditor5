from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dictionary import views

urlpatterns = [
    path('', views.home, name='home'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('auth/', include('user_auth.urls')),
    path('passage/', include('passage.urls')),
    path('word/', include('word.urls')),
    path('note/', include('note.urls')),
    path('word-meaning/', include('word_meaning.urls')),
    path('example/', include('example.urls')),
    path('settings/', include('settings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
