from django.contrib import admin
from django.utils.html import format_html
from .models import Photo, FacialLandmarks
import json

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'image', 'uploaded_at', 'get_id_number', 'visible')
    search_fields = ('user__username', 'uploaded_at')
    list_filter = ('visible',)

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

    def get_id_number(self, obj):
        return obj.profile.id_number

    get_id_number.short_description = 'ID Number'

class FacialLandmarksAdmin(admin.ModelAdmin):
    list_display = ('get_photo_image', 'created_at', 'get_user_id_number', 'formatted_data')
    search_fields = ('photo__user__username', 'photo__profile__id_number')
    list_filter = ('created_at',)

    def get_photo_image(self, obj):
        return obj.photo.image.name

    get_photo_image.short_description = 'Photo'

    def get_user_id_number(self, obj):
        return obj.photo.profile.id_number

    get_user_id_number.short_description = 'User ID Number'

    def formatted_data(self, obj):
        try:
            landmarks_data = json.loads(obj.data)
        except json.JSONDecodeError:
            return "Invalid JSON"
        
        if not landmarks_data:
            return "-"
        
        html = "<table style='border: 1px solid black; border-collapse: collapse;'>"
        
        if isinstance(landmarks_data, list):
            for i, landmark in enumerate(landmarks_data):
                html += f"<tr><th colspan='2' style='border: 1px solid black; padding: 5px;'>Face {i+1}</th></tr>"
                for key, value in landmark.items():
                    if key == 'landmarks':
                        html += f"<tr><td style='border: 1px solid black; padding: 5px;'>{key}</td><td style='border: 1px solid black; padding: 5px;'>{len(value)} points</td></tr>"
                    else:
                        html += f"<tr><td style='border: 1px solid black; padding: 5px;'>{key}</td><td style='border: 1px solid black; padding: 5px;'>{value}</td></tr>"
        elif isinstance(landmarks_data, dict):
            for key, value in landmarks_data.items():
                if key == 'landmarks':
                    html += f"<tr><td style='border: 1px solid black; padding: 5px;'>{key}</td><td style='border: 1px solid black; padding: 5px;'>{len(value)} points</td></tr>"
                else:
                    html += f"<tr><td style='border: 1px solid black; padding: 5px;'>{key}</td><td style='border: 1px solid black; padding: 5px;'>{value}</td></tr>"
        else:
            return "Unexpected data format"
        
        html += "</table>"
        return format_html(html)

    formatted_data.short_description = 'Facial Landmarks'

admin.site.register(Photo, PhotoAdmin)
admin.site.register(FacialLandmarks, FacialLandmarksAdmin)