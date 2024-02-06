from django.shortcuts import render

from .form import CreateUserFrom


def base(req):
    return render(req, 'main/base.html')


def reg(req):
    form = CreateUserFrom()
    # form.username = "req.POST['email']"

    if req.method == 'POST':
        print(req.POST['email'])
        # form.username = 'jjljlbj'
        form = CreateUserFrom(req.POST)

        if form.is_valid():
            # form.initial.username = req.POST['email']
            form.save()

    ctx = {'form': form}
    return render(req, 'main/auth/reg.html', ctx)
