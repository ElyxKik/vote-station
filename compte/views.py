from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from compte.forms import LoginForm, NewUserForm



def signup(request):
    message = ''
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto login user
            login(request, user)
        else:
            message = "L'un des champs ci-dessous n'a pas été bien rempli"
    return render(request, 'signup.html', {'form': form, 'message': message})


def login_user(request):
    form = LoginForm()
    message = ''
    user = request.user
    if user.is_authenticated == False:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    message = 'Identifiants invalides'
    else:
        return redirect('home')
    return render(request, 'login.html', context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')
