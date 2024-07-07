from django.shortcuts import render, redirect
from .models import Accounts
from .forms import CreateNewAccount
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(response):
    
    return render(response, "main/home.html", {})

# creating new accounts and showing account data
@login_required(login_url="/accounts/")
def accounts(response):
    # user clicked ADD ACCOUNT
    if response.method == "POST":
        form = CreateNewAccount(response.POST)
        # try to create a new account
        if form.is_valid():
            n = form.cleaned_data["name"].upper()
            b = form.cleaned_data["balance"]
            new = Accounts(account_name=n, balance=b)
            new.save()

            # create account
            try:
                response.user.accounts.add(new)
            # catch duplicates
            except IntegrityError as e:
                print(response.user.accounts.all)
                return redirect("/accounts")
            
        return redirect("/accounts")
    else:
        # returns a form for creating new account data
        form = CreateNewAccount()

    return render(response, "main/accounts.html", {"form": form})