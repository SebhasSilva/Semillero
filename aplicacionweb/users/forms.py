from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    contact_number = forms.CharField(max_length=15, required=True, help_text='Required.')
    birth_date = forms.DateField(required=True, help_text='Required. Format: YYYY-MM-DD')
    address = forms.CharField(max_length=255, required=True, help_text='Required.')
    city = forms.CharField(max_length=100, required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'contact_number', 'birth_date', 'address', 'city', 'password1', 'password2')