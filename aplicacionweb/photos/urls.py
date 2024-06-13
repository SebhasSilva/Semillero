from django.urls import path
from .views import upload_photos, PhotoUploadView, PhotoListView, PhotoDeleteView

urlpatterns = [
    path('upload/', PhotoUploadView.as_view(), name='photo_upload_api'),  # Para la API de subida
    path('list/', PhotoListView.as_view(), name='photo_list'),  # Para listar las fotos
    path('upload/ajax/', upload_photos, name='upload_photos'),  # Para la subida vía Ajax
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='delete_photo'),  # Para eliminar una foto
]