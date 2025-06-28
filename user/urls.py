from django.urls import path
from user import views

urlpatterns = [
    path('unique-username/<str:username>/', views.unique_username, name='unique-username'),
]
