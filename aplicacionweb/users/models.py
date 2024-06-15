from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
import random

# Custom User model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default='0000000000')
    birth_date = models.DateField(default=date.today)
    address = models.CharField(max_length=255, default='Sin dirección')
    city = models.CharField(max_length=100, default='Sin ciudad')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'profile'):
            Profile.objects.create(user=self)

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=6, unique=True, blank=True)
    photos = models.ManyToManyField('photos.Photo', blank=True)

    def save(self, *args, **kwargs):
        if not self.id_number:
            self.id_number = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            id_number = ''.join(random.choices('123456789', k=6))
            if not Profile.objects.filter(id_number=id_number).exists():
                return id_number

# Street Person model
class StreetPerson(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    birth_city = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

# Street Person History model
class StreetPersonHistory(models.Model):
    street_person = models.ForeignKey(StreetPerson, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    changes = models.JSONField()