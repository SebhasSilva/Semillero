from django.urls import path
from .views import PhotoUploadView, PhotoListView

urlpatterns = [
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('', PhotoListView.as_view(), name='photo_list'),
]
