from django.urls import path
from settings import views

urlpatterns = [
    path('get-general-settings/', views.get_general_settings, name='get-general-settings'),
    path('get-user-settings/', views.get_user_settings, name='get-user-settings'),
    path('get-user-settings-json/', views.get_user_settings_json, name='get-user-settings-json'),
    # path('edit-example/<int:id>/', views.edit_example, name='edit-example'),
    # path('delete-example/<int:id>/', views.delete_example, name='delete-example'),
]