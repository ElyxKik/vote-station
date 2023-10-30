from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
import string
from django.contrib.auth.hashers import make_password

from compte.forms import LoginForm
from compte.models import User
from vote.models import Electeur


def generate_random_username():
    length = 6
    characters = string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_password():
    length = 10
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def signup(request):
    return render(request, 'signup.html')


def new_electeur(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        post_nom = request.POST.get('post_nom')
        username = generate_random_username()
        password = generate_random_password()
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        user.save()
        electeur = Electeur.objects.create(user=user, nom=nom, post_nom=post_nom, prenom=prenom)
        electeur.save()
        return HttpResponse(f"Compte créé avec succès.Nom d'utilisateur : {username} | Mot de passe : {password}")



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
