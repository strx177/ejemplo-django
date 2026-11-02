from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #incluir todas las urls de las aplicaciones
    path('', include('catalogo.urls')),
]
#permitir acceder desde el navegador a las imagenes u 
# otros archivos guardados en MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

