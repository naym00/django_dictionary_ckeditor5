from django.urls import path
from passage import views

urlpatterns = [
    path('get-passages/', views.get_passages, name='get-passages'),
    path('add-passage/', views.add_passage, name='add-passage'),
    path('get-passage-using-id/<int:id>/', views.get_passage_using_id, name='get-passage-using-id'),
    # path('delete-example/<int:id>/', views.delete_example, name='delete-example'),
]