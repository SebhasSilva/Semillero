# photos/forms.py

from django import forms
from .models import Photo

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']  # Ajusta los campos según tus necesidades
