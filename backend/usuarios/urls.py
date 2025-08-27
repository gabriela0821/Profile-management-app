"""
URLs para la app usuarios
"""
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('token/refresh/', views.refresh_token, name='token_refresh'),
    
    # Perfil
    path('perfil/', views.get_profile, name='get_profile'),
    path('usuario/perfil/', views.update_profile, name='update_profile'),
    path('perfil/foto/', views.upload_profile_photo, name='upload_photo'),
    
    # Utilidades
    path('user/info/', views.user_info, name='user_info'),
    path('status/', views.api_status, name='api_status'),
]