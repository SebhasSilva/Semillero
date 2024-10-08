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
from .models import CustomUser, StreetPerson, StreetPersonHistory, Notification, Profile
import uuid
from .utils import generate_common_id

def home(request):
    return render(request, 'users/home.html')

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

    # Obtener notificaciones no leídas
    notifications = Notification.objects.filter(profile=request.user.profile, is_read=False)
    notification_count = notifications.count()

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
                    if not street_person_data.common_id:
                        street_person_data.common_id = generate_common_id()
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
        elif 'mark_notifications_read' in request.POST:
            # Marcar todas las notificaciones como leídas
            notifications.update(is_read=True)
            return redirect('profile')

    photos = Photo.objects.filter(user=request.user, visible=True)

    return render(request, 'users/profile.html', {
        'photo_form': photo_form,
        'street_person_form': street_person_form,
        'photos': photos,
        'street_person': street_person,
        'notifications': notifications,
        'notification_count': notification_count
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# NUEVO CÓDIGO: Añade esta nueva función al final del archivo
@csrf_exempt
@require_POST
def receive_notification(request):
    try:
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        message = data.get('message')

        # Añade esta validación
        if not profile_id or not message:
            return JsonResponse({"status": "error", "message": "Missing profile_id or message"}, status=400)
        
        profile = Profile.objects.get(id_number=profile_id)
        Notification.objects.create(profile=profile, message=message)
        
        return JsonResponse({"status": "success"}, status=201)
    except Profile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)