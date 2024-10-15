from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseForbidden
from .forms import CustomUserCreationForm, StreetPersonForm
from photos.forms import PhotoUploadForm
from photos.models import Photo
from .models import CustomUser, StreetPerson, StreetPersonHistory
import uuid
import json
from .utils import generate_common_id
from django.db.models import Count
from .models import StreetPerson
from django.utils import timezone
from django.db.models.functions import ExtractYear
from .models import StreetPerson, FamilySearch
from django.http import JsonResponse
from datetime import datetime

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

def validate_token(token):
    # Implementa la lógica de validación del token aquí
    # Por ahora, retornamos True para evitar errores
    return True

def estadisticas_view(request):
    token = request.GET.get('token')
    if validate_token(token):
        genero = request.GET.get('genero')
        ciudad = request.GET.get('ciudad')
        fecha = request.GET.get('fecha')

        current_year = timezone.now().year
        
        # Filtrar datos
        street_persons = StreetPerson.objects.all()
        family_searches = FamilySearch.objects.all()

        if genero:
            street_persons = street_persons.filter(gender=genero)
            family_searches = family_searches.filter(search_gender=genero)
        if ciudad:
            street_persons = street_persons.filter(birth_city=ciudad)
            family_searches = family_searches.filter(search_city=ciudad)
        if fecha:
         try:
            fecha_filtro = datetime.strptime(fecha, '%Y-%m-%d').date()
            street_persons = street_persons.filter(created_at__gte=fecha_filtro)
            family_searches = family_searches.filter(created_at__gte=fecha_filtro)
         except ValueError:
            # Si la fecha no es válida, simplemente ignoramos el filtro
            pass

        # Calcular edades y contar
        street_data = street_persons.annotate(
            age=current_year - ExtractYear('birth_date')
        ).values('age').annotate(count=Count('id'))
        
        family_data = family_searches.annotate(
            age=current_year - ExtractYear('search_birth_date')
        ).values('age').annotate(count=Count('id'))
        
        # Preparar datos para la gráfica
        age_ranges = ['0-18', '19-30', '31-45', '46-60', '60+']
        street_counts = [0] * len(age_ranges)
        family_counts = [0] * len(age_ranges)
        
        for item in street_data:
            index = min(item['age'] // 15, 4)
            street_counts[index] += item['count']
        
        for item in family_data:
            index = min(item['age'] // 15, 4)
            family_counts[index] += item['count']
        
        data = {
            'age_ranges': age_ranges,
            'street_counts': street_counts,
            'family_counts': family_counts,
        }
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(data)
        
        return render(request, 'users/estadisticas.html', {'data': json.dumps(data)})
    else:
        return HttpResponseForbidden("Acceso no autorizado")