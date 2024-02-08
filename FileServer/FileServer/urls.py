from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from FileServer import settings
from main.views import *
# from . import views

handler404 = error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    # pages
    path('', index, name='index'),
    path('auth/reg/', regPage, name='reg'),
    path('auth/login/', loginPage, name='login'),
    path('auth/logout/', logoutUser, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)