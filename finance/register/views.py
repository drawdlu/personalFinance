from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .token import account_activation_token

# activate when link is pressed
def activate(response, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(response, "Successfully confirmed email, you can now login to your account")
    else:
        messages.error(response, "Activation link is invalid.")

    return redirect('/')

# send activation email
def emailActivation(response, new_user, to_email):
    mailSubject = "Activate your user account."
    mailMessage = render_to_string("activateAccount.html", {
        'user': new_user.username,
        'domain': get_current_site(response).domain,
        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
        'token': account_activation_token.make_token(new_user),
        "protocol": 'https' if response.is_secure() else 'http'
    })

    email = EmailMessage(mailSubject, mailMessage, to=[to_email])

    if email.send():
        messages.success(response, "Please check your inbox and click the account activation link to complete your registration")
    else:
        messages.error(response, "Problem sending to your email, kindly check if you typed it correctly")

# register new user
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            emailActivation(response, new_user, form.cleaned_data.get('email'))
            return redirect("/")
    else: 
        form = RegisterForm()
    return render(response, "register.html", {"form": form})