from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import dynamic_sitemap_xml_view

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('sitemap.xml', dynamic_sitemap_xml_view, name='root-sitemap-xml'),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
