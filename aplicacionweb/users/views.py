from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, StreetPersonForm
from photos.forms import PhotoUploadForm
from photos.models import Photo
from .models import CustomUser, StreetPerson, StreetPersonHistory

# Vista para la página de inicio
def home(request):
    return render(request, 'users/home.html')

# Vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
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
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Vista para el logout de usuarios
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

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

# Vista para el perfil de usuario con subida de fotos y gestión de StreetPerson
@login_required
def profile(request):
    photo_form = PhotoUploadForm()
    street_person_form = StreetPersonForm()

    if request.method == 'POST':
        if 'photo_form_submit' in request.POST:
            photo_form = PhotoUploadForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.user = request.user
                photo.profile = request.user.profile  # Asignar el perfil del usuario a la foto
                photo.save()
                return redirect('profile')
        elif 'street_person_form_submit' in request.POST:
            street_person_form = StreetPersonForm(request.POST)
            if street_person_form.is_valid():
                street_person_data = street_person_form.save(commit=False)
                street_person_data.profile = request.user.profile  # Asignar el perfil del usuario
                street_person_data.save()

                # Guardar el historial de cambios
                StreetPersonHistory.objects.create(
                    street_person=street_person_data,
                    modified_by=request.user,
                    changes={
                        'first_name': street_person_data.first_name,
                        'last_name': street_person_data.last_name,
                        'birth_date': street_person_data.birth_date,
                        'birth_city': street_person_data.birth_city,
                        'alias': street_person_data.alias,
                        'gender': street_person_data.gender,
                    }
                )

                return redirect('profile')

    photos = Photo.objects.filter(user=request.user, visible=True)  # Filtrar solo fotos visibles
    street_person = StreetPerson.objects.filter(profile__user=request.user).last()

    return render(request, 'users/profile.html', {
        'photo_form': photo_form,
        'street_person_form': street_person_form,
        'photos': photos,
        'street_person': street_person
    })

# Vista para eliminar una foto solo visualmente
@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    if request.method == 'POST':
        photo.visible = False  # Marcar la foto como no visible en lugar de eliminarla físicamente
        photo.save()
        return redirect('profile')
    return render(request, 'users/profile.html', {
        'photo_form': PhotoUploadForm(),
        'street_person_form': StreetPersonForm(),
        'photos': Photo.objects.filter(user=request.user, visible=True),  # Filtrar solo fotos visibles
        'street_person': StreetPerson.objects.filter(profile__user=request.user).last()
    })