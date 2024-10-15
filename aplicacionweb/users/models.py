from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
from django.conf import settings

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default='0000000000')
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    acepto_tratamiento = models.BooleanField(
        default=False,
        help_text="Indica si el usuario ha aceptado el tratamiento de sus datos personales."
    )
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            Profile.objects.create(user=self)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    id_number = models.CharField(max_length=6, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id_number:
            self.id_number = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            id_number = ''.join(random.choices('123456789', k=6))
            if not Profile.objects.filter(id_number=id_number).exists():
                return id_number

class StreetPerson(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='street_persons')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    birth_city = models.CharField(max_length=100)
    alias = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    common_id = models.CharField(max_length=50, unique=True, null=True)

    def to_mongo_dict(self):
        return {
            'nombre': self.first_name,
            'apellido': self.last_name,
            'ciudad': self.birth_city,
            'genero': self.gender,
            'common_id': self.common_id
        }

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StreetPersonHistory(models.Model):
    street_person = models.ForeignKey(StreetPerson, on_delete=models.CASCADE, related_name='history')
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    changes = models.JSONField()

    def __str__(self):
        return f"History for {self.street_person} at {self.modified_at}"

class FamilySearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_name = models.CharField(max_length=100)
    search_birth_date = models.DateField()
    search_gender = models.CharField(max_length=10)
    search_last_seen = models.DateField()
    search_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Búsqueda de {self.search_name} por {self.user.username}"

# Importar aquí para evitar la circularidad
from photos.models import Photo
Profile.add_to_class('photos', models.ManyToManyField(Photo, blank=True, related_name='profile_photos'))