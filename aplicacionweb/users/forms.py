from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StreetPerson

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ únicamente.'
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'birth_date',
            'address',
            'city',
            'password1',
            'password2'
        )

class StreetPersonForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombres')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True, label='Fecha de nacimiento')
    birth_city = forms.CharField(max_length=100, required=True, label='Ciudad de nacimiento')
    alias = forms.CharField(max_length=100, required=True, label='Alias')

    class Meta:
        model = StreetPerson
        fields = ['first_name', 'last_name', 'birth_date', 'birth_city', 'alias']