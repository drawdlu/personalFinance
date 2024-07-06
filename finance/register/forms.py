from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm): # inherits attributes of UserCreationForm

    class Meta: # allows this register form to be saved into users database
        model = User
        fields = ["username", "password1", "password2"] # layout where fields will be