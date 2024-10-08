from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, StreetPersonForm
from photos.forms import PhotoUploadForm
from photos.models import Photo
from .models import CustomUser, StreetPerson, StreetPersonHistory
import uuid
from .utils import generate_common_id

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.acepto_tratamiento = form.cleaned_data.get('acepto_tratamiento')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'users/password_reset_email.html'
    form_class = PasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_sent.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = SetPasswordForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

@login_required
def profile(request):
    photo_form = PhotoUploadForm()
    street_person = StreetPerson.objects.filter(profile__user=request.user).last()
    street_person_form = StreetPersonForm(instance=street_person)

    if street_person_form.is_valid():
        street_person_data = street_person_form.save(commit=False)
        if not street_person_data.common_id:
            street_person_data.common_id = generate_common_id()  # Implementa esta función
        street_person_data.save()

    if request.method == 'POST':
        if 'photo_form_submit' in request.POST:
            photo_form = PhotoUploadForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.user = request.user
                photo.profile = request.user.profile
                photo.save()
                return redirect('profile')
        elif 'street_person_form_submit' in request.POST:
            print("Formulario de StreetPerson enviado")
            street_person_form = StreetPersonForm(request.POST, instance=street_person)
            if street_person_form.is_valid():
                print("Formulario válido. Datos:", street_person_form.cleaned_data)
                try:
                    street_person_data = street_person_form.save(commit=False)
                    street_person_data.profile = request.user.profile
                    street_person_data.save()
                    print(f"StreetPerson guardado con ID: {street_person_data.id}")

                    # Guardar el historial de cambios
                    changes = {field: str(street_person_form.cleaned_data[field]) for field in street_person_form.changed_data}
                    StreetPersonHistory.objects.create(
                        street_person=street_person_data,
                        modified_by=request.user,
                        changes=changes
                    )
                    print("StreetPersonHistory creado exitosamente")

                    return redirect('profile')
                except Exception as e:
                    print(f"Error al guardar StreetPerson: {str(e)}")
            else:
                print("Formulario no válido. Errores:", street_person_form.errors)

    photos = Photo.objects.filter(user=request.user, visible=True)

    return render(request, 'users/profile.html', {
        'photo_form': photo_form,
        'street_person_form': street_person_form,
        'photos': photos,
        'street_person': street_person
    })

@login_required
@csrf_protect
def delete_photo(request, photo_id):
    print(f"Request to delete photo with id: {photo_id}")
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        photo.visible = False
        photo.save()
        print(f"photo with id {photo_id} marked as not visible")
        return redirect('profile')
    return HttpResponse("Photo not deleted")