from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Folder


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
