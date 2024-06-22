from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'image', 'uploaded_at', 'get_id_number')
    search_fields = ('user__username', 'uploaded_at')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

    def get_id_number(self, obj):
        return obj.user.profile.id_number  # Accedemos al id_number del perfil del usuario

    get_id_number.short_description = 'ID Number'

admin.site.register(Photo, PhotoAdmin)
