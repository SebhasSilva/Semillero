from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    
    # Añadir otros campos necesarios
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'profile'):
            Profile.objects.create(user=self)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=6, unique=True, blank=True)
    photos = models.ManyToManyField('Photo')

    def save(self, *args, **kwargs):
        if not self.id_number:
            self.id_number = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            id_number = ''.join(random.choices('123456789', k=6))
            if not Profile.objects.filter(id_number=id_number).exists():
                return id_number

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)