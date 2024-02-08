from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from FileServer import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # pages
    path('', base, name='index'),
    path('auth/reg/', regPage, name='reg'),
    path('auth/log/', logPage, name='log')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
