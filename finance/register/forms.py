from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm): # inherits attributes of UserCreationForm

    class Meta: # allows this register form to be saved into users database
        model = User
        fields = ["username", "email", "password1", "password2"] # layout where fields will be
    
    # make email required and change label
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].label = "Email Address"
    
    # check if email is unique to user
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered")
       return self.cleaned_data