from django.contrib import admin
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'image', 'uploaded_at')
    search_fields = ('user__username', 'uploaded_at')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

admin.site.register(Photo, PhotoAdmin)