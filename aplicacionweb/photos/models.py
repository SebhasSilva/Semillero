from django.conf import settings
from django.db import models
from users.models import Profile
from django.utils.safestring import mark_safe
import json

class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_photos')
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)  # Campo para controlar la visibilidad de la foto

    def __str__(self):
        return f'{self.user.username} - {self.image.name}'

    @property
    def id_number(self):
        return self.profile.id_number

class FacialLandmarks(models.Model):
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE, related_name='landmarks')
    data = models.JSONField()  # Campo para almacenar los puntos faciales en formato JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Landmarks for {self.photo.image.name}'

    def formatted_data(self):
        data_dict = json.loads(self.data)
        formatted = json.dumps(data_dict, indent=4)
        return mark_safe(f'<pre>{formatted}</pre>')
    
    formatted_data.short_description = 'Formatted Data'