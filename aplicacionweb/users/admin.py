from django.contrib import admin
from .models import CustomUser, Profile, Photo

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

# Registro del modelo Photo en el administrador
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'image', 'uploaded_at')
    search_fields = ('user__username', 'uploaded_at')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

admin.site.register(Photo, PhotoAdmin)