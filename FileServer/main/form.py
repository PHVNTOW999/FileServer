from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserFrom(UserCreationForm):
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