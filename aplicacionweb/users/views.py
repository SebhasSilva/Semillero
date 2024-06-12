# users/views.py

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

# Vista para la página de inicio
def home(request):
    return render(request, 'users/home.html')

# Vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            username = form.cleaned_data.get('email')  # Cambiado a 'email' ya que el formulario utiliza el email para autenticación
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Vista para el login de usuarios
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('photo_upload')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Vista para el logout de usuarios
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista personalizada para el reseteo de contraseña
class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'users/password_reset_email.html'
    form_class = PasswordResetForm

# Vista personalizada para la confirmación de envío de email para reseteo de contraseña
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_sent.html'

# Vista personalizada para la confirmación del reseteo de contraseña
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = SetPasswordForm

# Vista personalizada para la finalización del reseteo de contraseña
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'