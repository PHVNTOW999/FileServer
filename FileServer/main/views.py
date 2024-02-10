from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .form import CreateUserFrom
from .models import Folder, File


# pages
def indexPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    else:
        return redirect('reg')


def foldersPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Folder.objects.create(name=request.POST.get('name'), user=request.user).save()
            return redirect(request.path)

        folders = Folder.objects.filter(user=request.user)
        ctx = {'folders': folders}

        return render(request, 'main/folders.html', ctx)

    else:
        return redirect('reg')


def folderPage(request, uuid):
    if request.user.is_authenticated:

        files = File.objects.filter(folders__uuid=uuid, user=request.user)
        ctx = {'files': files}

        return render(request, 'main/folder.html', ctx)

    else:
        return redirect('reg')


def del_folder(request, uuid):
    if request.user.is_authenticated:
        Folder.objects.get(uuid=uuid, user=request.user).delete()

        return redirect('folders')

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

        return render(request, 'main/auth/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


# Error 404 page
def error_404(request, exception=None):
    return redirect('index')
