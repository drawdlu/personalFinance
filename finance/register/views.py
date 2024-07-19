from django.shortcuts import render, redirect
from .forms import RegisterForm, SetPasswordForm, PasswordResetForm
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
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from main.models import UserProfile

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
    # handle instances when user types this on url while logged in
    if response.user.is_authenticated:
        return redirect('/')
    
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            # create new user and send email
            new_user = form.save(commit=False)
            new_user.is_active=False
            new_user.save()
            emailActivation(response, new_user, form.cleaned_data.get('email'))

            # create user profile
            new = UserProfile(user=new_user)
            new.save()

            return redirect("/")
    else: 
        form = RegisterForm()
    return render(response, "register.html", {"form": form})

# allow users to change password
@login_required(login_url="/login/")
def change_password(response):
    user = response.user

    if response.method == 'POST':
        form = SetPasswordForm(user, response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, "Successfully changed your password. Please login to continue")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(response, error)

    form = SetPasswordForm(user)
    return render(response, "passwordResetConfirm.html", {"form": form})

# allow users to change password through their email
def password_reset(response):
    # handle instances when user types this on url while logged in
    if response.user.is_authenticated:
        return redirect('/')
        
    if response.method == 'POST':
        form = PasswordResetForm(response.POST)
        if form.is_valid():
            userEmail = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=userEmail)).first()
            if associated_user:
                subject = "Password reset request"
                message = render_to_string("resetPassword.html", {
                    'user': associated_user,
                    'domain': get_current_site(response).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if response.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[userEmail])
                if email.send():
                    messages.success(response, "Please check your email for password reset instructions")
                else:
                    messages.error(response, "Problem sending reset password email")
                
                return redirect('/')
            else:
                messages.info(response, "The email you entered is not associated with any acount")
                return render(response, "passwordReset.html", {"form": form})
            
        else:
            for error in list(form.errors.values()):
                messages.error(response, error)

    form = PasswordResetForm()
    return render(response, "passwordReset.html", {"form": form})

# email password reset link pressed
def passwordResetConfirm(response, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if response.method == 'POST':
            form = SetPasswordForm(user, response.POST)
            if form.is_valid():
                form.save()
                messages.success(response, "Your password has succesfully been changed")
                return redirect('/')
            else:
                for error in list(form.errors.values()):
                    messages.error(response, error)
            
        form = SetPasswordForm(user)
        return render(response, "passwordReset.html", {"form": form})
    else:
        messages.error(response, "Activation link is invalid.")

    messages.error(response, "Something went wrong, redirecting back to login page.")
    return redirect('/')