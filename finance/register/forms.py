from django import forms
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from main.models import UserProfile

class RegisterForm(UserCreationForm): # inherits attributes of UserCreationForm

    class Meta: # allows this register form to be saved into users database
        model = User
        fields = ["username", "email", "password1", "password2"] # layout where fields will be
    
    # make email required and change label
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].label = "Email Address"
    
    # make sure email is unique to user
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered")
       return self.cleaned_data
    
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['password1', 'password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class ChangeCurrency(forms.Form):
    currency_choices = (
        ("", "--------"),
        ("$", "Dollar"), 
        ("€", "Euro"), 
        ("£", "Pound"),
        ("¥", "Yen"),
        ("₣", "Franc"),
        ("₹", "Rupee"),
        ("د. ك'", "Dinar"),
        ("₱", "Peso")
    )
    currency = forms.ChoiceField(choices=currency_choices)