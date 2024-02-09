from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .form import CreateUserFrom


def indexPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    else:
        return redirect('reg')


def foldersPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/files.html')

    else:
        return redirect('reg')


def filesPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/files.html')

    else:
        return redirect('reg')

# auth pages


def regPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    else:
        form = CreateUserFrom()

        if request.method == 'POST':

            try:
                if User.objects.get(email=request.POST['email']):
                    messages.error(request,
                                   f'Account with that Email - {User.objects.get(email=request.POST["email"]).email}, '
                                   f' already was created!')

                    ctx = {'form': form}
                    return render(request, 'main/auth/reg.html', ctx)

            except User.DoesNotExist:
                form = CreateUserFrom(request.POST)

                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()

                    messages.success(request, 'Account is created!')

                    ctx = {'form': form}
                    return render(request, 'main/auth/reg.html', ctx)

        ctx = {'form': form}
        return render(request, 'main/auth/reg.html', ctx)


def loginPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                messages.error(request, 'Username or Password is incorrect')

        ctx = {'form': 'ooo'}
        return render(request, 'main/auth/login.html', ctx)


def logoutUser(request):
    logout(request)
    return redirect('login')


# Error 404 page
def error_404(request, exception=None):
    return redirect('index')
