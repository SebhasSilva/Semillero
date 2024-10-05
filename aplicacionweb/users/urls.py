from django.urls import path
from .views import (
    register, login_view, logout_view, profile, delete_photo, 
    CustomPasswordResetView, CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
    receive_notification  # Añade esta importación
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('photos/delete/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Añade esta nueva ruta
    path('receive_notification/', receive_notification, name='receive_notification'),
]