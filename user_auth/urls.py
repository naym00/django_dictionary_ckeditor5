from django.urls import path
from user_auth import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('set-password/', views.set_new_password, name='set-password'),
    path('logout/', views.user_logout, name='logout'),
]
