from django.urls import path
from passage import views

urlpatterns = [
    path('get-passages/', views.get_passages, name='get-passages'),
    path('add-passage/', views.add_passage, name='add-passage'),
    path('get-passage-using-id/<int:passageid>/', views.get_passage_using_id, name='get-passage-using-id'),
    path('remove-passage-from-my-list/<int:passageid>/', views.remove_passage_from_my_list, name='remove-passage-from-my-list'),
    path('add-passage-to-your-list/<int:passageid>/', views.add_passage_to_your_list, name='add-passage-to-your-list'),
]