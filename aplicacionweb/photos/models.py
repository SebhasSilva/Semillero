from django.conf import settings
from django.db import models
from users.models import Profile

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