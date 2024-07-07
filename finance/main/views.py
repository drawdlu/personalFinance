from django.shortcuts import render, redirect
from .models import Accounts, Category, Debit, Credit
from .forms import CreateNewAccount, CreateNewCategory, CreateNewDebit
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here

# main page showing current months balance sheet
@login_required(login_url="/login/")
def home(response):
    if response.method == "POST":
        formC = CreateNewCategory(response.POST)
        formD = CreateNewDebit(response.POST)
        
        # pressed add category button
        if "add_category" in response.POST:
        # try to create new category
            if formC.is_valid():
                n = formC.cleaned_data["category_name"].upper()
                new = Category(category_name=n)
                new.save()

                # create category
                try:
                    response.user.category.add(new)
                except IntegrityError as e:
                    print(e)

        # pressed add expense button
        if "add_expense" in response.POST:
            # gate data from form and save it 
            if formD.is_valid():
                amount = formD.cleaned_data["amount"]
                description = formD.cleaned_data["description"]
                date = formD.cleaned_data["date"]
                acc = formD.cleaned_data["account"]
                ca = formD.cleaned_data["category"]
                account = Accounts.objects.get(account_name=acc)
                category = Category.objects.get(category_name=ca)
                new = Debit(amount=amount, description=description, account=account, category=category, date=date)
                new.save()

                # create debit
                response.user.debit.add(new)
                # update account
                account.balance -= amount
                account.save()
            else:
                print("not valid expense")

        # pressed add credit button
        if "add_credit" in response.POST:
            # gate data from form and save it 
            if formD.is_valid():
                amount = formD.cleaned_data["amount"]
                description = formD.cleaned_data["description"]
                date = formD.cleaned_data["date"]
                acc = formD.cleaned_data["account"]
                ca = formD.cleaned_data["category"]
                account = Accounts.objects.get(account_name=acc)
                category = Category.objects.get(category_name=ca)
                new = Credit(amount=amount, description=description, account=account, category=category, date=date)
                new.save()

                # create debit
                response.user.credit.add(new)
                # update account
                account.balance += amount
                account.save()
            else:
                print("not valid credit")
                
        return redirect("/")
    
    else:
        formC = CreateNewCategory()
        formD = CreateNewDebit()
    
    return render(response, "main/home.html", {"formC": formC, "formD":formD})

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
    else:
        # returns a form for creating new account data
        form = CreateNewAccount()

    return render(response, "main/accounts.html", {"form": form})