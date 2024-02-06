from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from .form import CreateUserFrom


def index(req):
    return render(req, 'main/index.html')


def reg(req):
    form = CreateUserFrom()

    if req.method == 'POST':
        form = CreateUserFrom(req.POST)

        if form.is_valid():
            form.save()

    ctx = {'form': form}
    return render(req, 'main/auth/reg.html', ctx)