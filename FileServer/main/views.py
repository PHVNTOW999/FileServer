from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .form import CreateUserForm, CreateFolderForm, CreateFileForm, UpdateFileForm
from .models import Folder, File


# pages
def indexPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    else:
        return redirect('reg')


def foldersPage(request):
    if request.user.is_authenticated:
        form = CreateFolderForm()

        if request.method == 'POST':
            form = CreateFolderForm(request.POST)

            if form.is_valid():
                new_folder = Folder(name=form.cleaned_data['name'], user=request.user)
                new_folder.save()

                return redirect(request.path)

        folders = Folder.objects.filter(user=request.user)
        ctx = {'data': {'folders': folders, 'form': form}}

        return render(request, 'main/folders/folders.html', ctx)

    else:
        return redirect('reg')


def folderPage(request, uuid):
    if request.user.is_authenticated:

        createForm = CreateFileForm(user=request.user)
        updateForm = UpdateFileForm(user=request.user)
        files = File.objects.filter(folder__uuid=uuid, user=request.user)

        folders = Folder.objects.filter(user=request.user)
        ctx = {'data': {'folders': folders, 'files': files, 'updateForm': updateForm, 'createForm': createForm}}

        return render(request, 'main/folders/folder.html', ctx)

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
        createForm = CreateFileForm(user=request.user)
        updateForm = UpdateFileForm(user=request.user)

        if request.method == 'POST':
            createForm = CreateFileForm(request.POST, request.FILES, user=request.user)

            if createForm.is_valid():
                new_file = File(
                    file=createForm.cleaned_data['file'],
                    name=createForm.cleaned_data['name'],
                    folder=createForm.cleaned_data['folder'],
                    user=request.user)

                new_file.save()

                return redirect('files')

        files = File.objects.filter(user=request.user)
        ctx = {'data': {'createForm': createForm, 'updateForm': updateForm, 'files': files}}

        return render(request, 'main/files/files.html', ctx)

    else:
        return redirect('reg')


def fileUpdate(request, uuid):
    if request.user.is_authenticated and request.method == 'POST':
        form = UpdateFileForm(request.POST, user=request.user)
        print(request.POST)

        if form.is_valid():
            print('gg')
            file = File.objects.get(uuid=uuid, user=request.user)
            file.folder = form.cleaned_data['folder']
            file.save()

            return redirect('files')
    else:
        return redirect('reg')


def del_file(request, uuid):
    if request.user.is_authenticated:
        File.objects.get(uuid=uuid, user=request.user).delete()

        return redirect('files')

    else:
        return redirect('reg')


# auth pages
def regPage(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    else:
        form = CreateUserForm()

        if request.method == 'POST':
            try:
                if User.objects.get(email=request.POST['email']):
                    messages.error(request,
                                   f'Account with that Email - {User.objects.get(email=request.POST["email"]).email}, '
                                   f' already was created!')

                    ctx = {'form': form}
                    return render(request, 'main/auth/reg.html', ctx)

            except User.DoesNotExist:
                form = CreateUserForm(request.POST)

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
