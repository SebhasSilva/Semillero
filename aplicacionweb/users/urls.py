from django.urls import path
from .views import (
    register, login_view, logout_view, profile, delete_photo, 
    CustomPasswordResetView, CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, estadisticas_view 
)

urlpatterns = [
    path('register/', register, name='register'),  # URL para el registro de usuarios
    path('login/', login_view, name='login'),  # URL para el login de usuarios
    path('logout/', logout_view, name='logout'),  # URL para el logout de usuarios
    path('profile/', profile, name='profile'),  # URL para el perfil de usuario
    path('photos/delete/<int:photo_id>/', delete_photo, name='delete_photo'),  # URL para eliminar una foto visualmente
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),  # URL para iniciar el reseteo de contraseña
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),  # URL de confirmación de envío de email para reseteo de contraseña
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # URL para confirmar el reseteo de contraseña
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # URL para completar el reseteo de contraseña
]   