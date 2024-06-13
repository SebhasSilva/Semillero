from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, login_view, logout_view, profile, CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns = [
    path('register/', register, name='register'),  # URL para el registro de usuarios
    path('login/', login_view, name='login'),  # URL para el login de usuarios
    path('logout/', logout_view, name='logout'),  # URL para el logout de usuarios
    path('profile/', profile, name='profile'),  # URL para el perfil de usuario
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),  # URL para iniciar el reseteo de contraseña
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),  # URL de confirmación de envío de email para reseteo de contraseña
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # URL para confirmar el reseteo de contraseña
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # URL para completar el reseteo de contraseña
]