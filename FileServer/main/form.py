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
    # queryset = Folder.objects.filter(user__email='test@gmail.com').values()
    queryset = None

    file = forms.FileField(label="File", required=True)
    name = forms.CharField(label="File's name", required=True)
    folder = forms.ModelChoiceField(queryset=queryset, empty_label=None, to_field_name='uuid', widget=forms.Select(),
                                    required=False)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.Folder = Folder.objects.all()
        super(CreateFileForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = self.queryset

    class Meta:
        model = File
        fields = ['file', 'name', ]
