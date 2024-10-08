from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StreetPerson

class CustomUserCreationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ únicamente.'
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)

    # Nuevo campo para aceptación de tratamiento de datos
    acepto_tratamiento = forms.BooleanField(
        required=True,
        label='Acepto el tratamiento de mis datos personales',
        help_text='Debes aceptar el tratamiento de datos para registrarte.'
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone_number',
            'birth_date', 'address', 'city', 'gender', 'password1', 'password2', 'acepto_tratamiento'
        )

    def clean_acepto_tratamiento(self):
        acepto = self.cleaned_data.get('acepto_tratamiento')
        if not acepto:
            raise forms.ValidationError("Debes aceptar el tratamiento de datos para registrarte.")
        return acepto

class StreetPersonForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    first_name = forms.CharField(max_length=30, required=True, label='Nombres')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Fecha de nacimiento'
    )
    birth_city = forms.CharField(max_length=100, required=True, label='Ciudad de nacimiento')
    alias = forms.CharField(max_length=50, required=False, label='Alias')  # Changed to match model definition
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, label='Género')  # Changed to match model definition

    class Meta:
        model = StreetPerson
        fields = ['first_name', 'last_name', 'birth_date', 'birth_city', 'alias', 'gender']

    def clean_alias(self):
        alias = self.cleaned_data.get('alias')
        if alias:
            return alias
        return ''  # Return empty string if alias is not provided

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender:
            return gender
        return None  # Return None if gender is not selected