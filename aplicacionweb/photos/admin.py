from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'image', 'uploaded_at', 'get_id_number', 'visible')
    search_fields = ('user__username', 'uploaded_at')
    list_filter = ('visible',)

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

    def get_id_number(self, obj):
        return obj.profile.id_number  # Accedemos al id_number del perfil

    get_id_number.short_description = 'ID Number'

admin.site.register(Photo, PhotoAdmin)