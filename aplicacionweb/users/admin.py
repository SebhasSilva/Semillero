# users/admin.py
from django.contrib import admin
from .models import CustomUser, Profile, Photo

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Photo)