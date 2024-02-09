import uuid as uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Folder(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(
        max_length=155,
        null=False,
        blank=False,
        verbose_name="Name"
    )

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        unique=False,
        on_delete=CASCADE
    )

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    def __str__(self):
        return self.name


class File(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    file = models.FileField(
        null=False,
        blank=False,
        upload_to='files',
        verbose_name='File'
    )

    folders = models.ManyToManyField(
        Folder,
        null=True,
        blank=True,
        verbose_name="Folders",
    )

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        unique=False,
        on_delete=CASCADE
    )

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.file}'
