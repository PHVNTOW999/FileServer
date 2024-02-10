from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from FileServer import settings
from main.views import *

handler404 = error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    # pages
    path('', indexPage, name='index'),
    # folders
    path('folders', foldersPage, name='folders'),
    path('folder/<uuid:uuid>', folderPage, name='folder'),
    path('folder/del/<uuid:uuid>', del_folder, name='del_folder'),
    # files
    path('files', filesPage, name='files'),
    # auth pages
    path('auth/reg/', regPage, name='reg'),
    path('auth/login/', loginPage, name='login'),
    path('auth/logout/', logoutUser, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
