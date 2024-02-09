from django.contrib import admin
from . import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'file',
        'uuid'
    )


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'uuid'
    )
