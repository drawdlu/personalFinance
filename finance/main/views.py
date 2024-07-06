from django.shortcuts import render, redirect
from .models import Accounts
from .forms import CreateNewAccount
from django.db import IntegrityError

# Create your views here.
def home(response):
    return render(response, "main/home.html", {})

def accounts(response):
    if response.method == "POST":
        form = CreateNewAccount(response.POST)
        
        if form.is_valid():
            n = form.cleaned_data["name"].upper()
            b = form.cleaned_data["balance"]
            new = Accounts(account_name=n, balance=b)
            new.save()

            # checking for duplicates
            try:
                response.user.accounts.add(new)
            except IntegrityError as e:
                print(response.user.accounts.all)
                return redirect("/accounts")
            
        return redirect("/accounts")
    else:
        form = CreateNewAccount()

    return render(response, "main/accounts.html", {"form": form})