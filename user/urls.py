from django.urls import path
from user import views

urlpatterns = [
    path('send-friend-request/<str:requested_to_id>/', views.send_friend_request, name='send-friend-request'),
    path('accept-friend-request/<str:user_id>/', views.accept_friend_request, name='accept-friend-request'),
    path('delete-friend-request/<str:user_id>/', views.delete_friend_request, name='delete-friend-request'),
    path('unique-username/<str:username>/', views.unique_username, name='unique-username'),
]
