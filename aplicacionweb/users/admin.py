from django.contrib import admin
from .models import CustomUser, Profile

# Registro del modelo CustomUser en el administrador con personalización
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'birth_date', 'address', 'city')
    search_fields = ('username', 'email', 'phone_number')

admin.site.register(CustomUser, CustomUserAdmin)

# Registro del modelo Profile en el administrador con personalización
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number')
    search_fields = ('user__username', 'id_number')

admin.site.register(Profile, ProfileAdmin)