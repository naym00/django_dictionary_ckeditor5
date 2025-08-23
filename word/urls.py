from django.urls import path
from word import views

urlpatterns = [
    path('get-words/', views.get_words, name='get-words'),
    path('add-word/', views.add_word, name='add-word'),
    path('edit-word/<int:id>/', views.edit_word, name='edit-word'),
    path('delete-word/<int:id>/', views.delete_word, name='delete-word'),
    path('edit-word-complexity-level/<int:id>/', views.edit_word_complexity_level, name='edit-word-complexity-level'),
    path('increment-blind-test-score/<int:id>/', views.increment_blind_test_score, name='increment-blind-test-score'),

    path('add-word-from-passage/<int:user_passage_id>/', views.add_word_from_passage, name='add-word-from-passage'),
]
