from django.urls import path
from passage import views

urlpatterns = [
    path('get-passages/', views.get_passages, name='get-passages'),
    path('add-passage/', views.add_passage, name='add-passage'),
    path('refetch-passages/', views.refetch_passages, name='refetch-passages'),
    path('remove-passages/', views.remove_passages, name='remove-passages'),
    path('edit-passage/<int:user_passage_id>/', views.edit_passage, name='edit-passage'),
    path('reset-passage/<int:user_passage_id>/', views.reset_passage, name='reset-passage'),
    path('get-passage-using-id/<int:user_passage_id>/', views.get_passage_using_id, name='get-passage-using-id'),
    path('remove-passage-from-my-list/<int:user_passage_id>/', views.remove_passage_from_my_list, name='remove-passage-from-my-list'),
    path('add-passage-to-your-list/<int:passage_id>/', views.add_passage_to_your_list, name='add-passage-to-your-list'),
]