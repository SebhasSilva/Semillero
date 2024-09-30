from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile, StreetPerson, StreetPersonHistory
import uuid

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'birth_date', 'address', 'city', 'gender', 'profile_id_number')
    search_fields = ('username', 'email', 'phone_number', 'profile__id_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('phone_number', 'birth_date', 'address', 'city', 'gender')}),
    )

    def profile_id_number(self, obj):
        return obj.profile.id_number if hasattr(obj, 'profile') else 'N/A'
    profile_id_number.short_description = 'Profile ID Number'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'user_id')
    search_fields = ('user__username', 'id_number', 'user__id')

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

@admin.register(StreetPerson)
class StreetPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'birth_city', 'alias', 'gender', 'created_at', 'profile_id_number', 'user_id', 'common_id')  # Añadido common_id
    search_fields = ('first_name', 'last_name', 'alias', 'profile__user__username', 'profile__id_number', 'profile__user__id', 'common_id')  # Añadido common_id
    list_filter = ('gender', 'birth_city')

    def profile_id_number(self, obj):
        return obj.profile.id_number
    profile_id_number.short_description = 'Profile ID Number'

    def user_id(self, obj):
        return obj.profile.user.id
    user_id.short_description = 'User ID'

    def generate_common_id(self):
        return str(uuid.uuid4())

    def save_model(self, request, obj, form, change):
        try:
            print("Intentando guardar StreetPerson")
            is_new = not obj.pk
            old_data = {} if is_new else {
                field: str(getattr(obj, field)) 
                for field in form.changed_data
            }
            
            if not obj.common_id:
                obj.common_id = self.generate_common_id()
            
            super().save_model(request, obj, form, change)
            print(f"StreetPerson guardado exitosamente. ID: {obj.pk}, Common ID: {obj.common_id}")
            
            new_data = {
                field: str(getattr(obj, field)) 
                for field in form.changed_data
            }
            
            changes = {
                field: {
                    'old': old_data.get(field),
                    'new': new_data.get(field)
                }
                for field in form.changed_data
            }
            
            history = StreetPersonHistory.objects.create(
                street_person=obj,
                modified_by=request.user,
                changes=changes
            )
            print(f"StreetPersonHistory creado exitosamente. ID: {history.pk}")
        
        except ValidationError as e:
            print(f"Error de validación al guardar StreetPerson: {str(e)}")
            raise
        except Exception as e:
            print(f"Error inesperado al guardar StreetPerson: {str(e)}")
            raise

@admin.register(StreetPersonHistory)
class StreetPersonHistoryAdmin(admin.ModelAdmin):
    list_display = ('street_person', 'modified_at', 'modified_by')
    search_fields = ('street_person__first_name', 'street_person__last_name', 'modified_by__username')
    readonly_fields = ('street_person', 'modified_at', 'modified_by', 'changes')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False