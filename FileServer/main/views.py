from django.shortcuts import render, redirect

from .form import CreateUserFrom


def base(req):
    return render(req, 'main/base.html')


def reg(req):
    form = CreateUserFrom()

    if req.method == 'POST':
        form = CreateUserFrom(req.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

    ctx = {'form': form}
    return render(req, 'main/auth/reg.html', ctx)
