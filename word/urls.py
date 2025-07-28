from django.urls import path
from word import views

urlpatterns = [
    path('words/', views.words, name='preview-words'),
    path('word-details/', views.word_details, name='word-details'),
    path('add-word/', views.add_word, name='add-word'),
    path('edit-word/<int:id>/', views.edit_word, name='edit-word'),
    path('delete-word/<int:id>/', views.delete_word, name='delete-word'),
    path('edit-word-complexity-level/<int:id>/', views.edit_word_complexity_level, name='edit-word-complexity-level'),

    path('add-word-from-passage/<int:user_passage_id>/', views.add_word_from_passage, name='add-word-from-passage'),
]
