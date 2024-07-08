from django.shortcuts import render, redirect
from .forms import RegisterForm
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save() # save new user into database
            messages.info(response, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password1"])
            login(response, new_user)
            return redirect("/")
    else: 
        form = RegisterForm()
    return render(response, "register.html", {"form": form})