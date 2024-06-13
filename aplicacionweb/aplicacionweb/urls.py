"""aplicacionweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el administrador de Django
    path('users/', include('users.urls')),  # Incluir las URLs de la aplicación de usuarios
    path('photos/', include('photos.urls')),  # Incluir las URLs de la aplicación de fotos
    path('', user_views.home, name='home'),  # Ruta principal que apunta a la vista home de los usuarios
]

# Si está en modo DEBUG, servir archivos estáticos y de medios desde el directorio del proyecto
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)