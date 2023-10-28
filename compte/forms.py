from django import forms
from django.contrib.auth.forms import UserCreationForm

from compte.models import User



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'email-address', 'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm', 'placeholder': 'ex: kikely'}), label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs=(
        {'id': 'password', 'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'})), label='Mot de passe')



class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
        Widget = {
            'username': forms.TextInput(attrs={'id': 'username', 'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm', 'placeholder': '', 'style': 'max-width: 300px;'}),
            'password1': forms.PasswordInput(attrs={'id': 'password', 'class': 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'}),
        }