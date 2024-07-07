from django.shortcuts import render, redirect
from .models import Accounts, Category
from .forms import CreateNewAccount, CreateNewCategory
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here

# main page showing current months balance sheet
@login_required(login_url="/login/")
def home(response):
    if response.method == "POST":
        form = CreateNewCategory(response.POST)

        # try to create new category
        if form.is_valid():
            n = form.cleaned_data["category_name"]
            new = Category(category_name=n)
            new.save()

            # create category
            try:
                response.user.category.add(new)
            except IntegrityError as e:
                print(e)
                return redirect("/")
    else:
        form = CreateNewCategory()
    
    return render(response, "main/home.html", {"form": form})

# creating new accounts and showing account data
@login_required(login_url="/login/")
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
                print(e)
                return redirect("/accounts")
            
        return redirect("/accounts")
    else:
        # returns a form for creating new account data
        form = CreateNewAccount()

    return render(response, "main/accounts.html", {"form": form})