from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Folder, File


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        exclude = ['username', ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class CreateFolderForm(forms.Form):
    name = forms.CharField(label="Folder's name", required=True)

    class Meta:
        model = Folder
        fields = ['name', ]


class CreateFileForm(forms.Form):
    file = forms.FileField(label="File", required=True)
    name = forms.CharField(label="File's name", required=True)
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(), empty_label='Select folder (option)', to_field_name='name',
                                    widget=forms.Select(), required=False, blank=True)

    class Meta:
        model = File
        fields = ['file', 'name', 'folder']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['folder'].queryset = Folder.objects.filter(user=user)
