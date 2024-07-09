from django.shortcuts import render, redirect
from .models import Accounts, Category, Debit, Credit
from .forms import CreateNewAccount, CreateNewCategory, CreateNewEntry
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .helper import get_values
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# Create your views here

# main page showing current months balance sheet
@login_required(login_url="/login/")
def home(response):
    if response.method == "POST":
        formC = CreateNewCategory(response.POST)
        formD = CreateNewEntry(response.POST)
        
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
                except IntegrityError:
                    messages.info(response, "Category already exists.")

        # pressed add expense button
        if "add_expense" in response.POST:
            # gate data from form and save it 
            if formD.is_valid():
                data = get_values(response, formD)
                new = Debit(amount=data["amount"], description=data["description"], account=data["account"], category=data["category"], date=data["date"])
                new.save()

                # create debit
                response.user.debit.add(new)
                # update account
                account = response.user.accounts.get(account_name=data["account"])
                account.balance -= data["amount"]
                account.save()

            else:
                print("not valid expense")

        # pressed add credit button
        if "add_credit" in response.POST:
            # gate data from form and save it 
            if formD.is_valid():
                data = get_values(response, formD)
                new = Credit(amount=data["amount"], description=data["description"], account=data["account"], category=data["category"], date=data["date"])
                new.save()

                # create debit
                response.user.credit.add(new)
                # update account
                account = response.user.accounts.get(account_name=data["account"])
                account.balance += data["amount"]
                account.save()
            else:
                print("not valid expense")
                
        return redirect("/")
    
    else:
        # create forms for user
        formC = CreateNewCategory()
        formD = CreateNewEntry()
        # make sure forms contains only categories and accounts of current user
        formD.fields["category"].queryset = response.user.category.all()
        formD.fields["account"].queryset = response.user.accounts.all()

    # filter and return current months debit and credit
    date = datetime.now()
    debitData = Debit.objects.filter(date__year=date.year,
                                     date__month=date.month)
    creditData = Credit.objects.filter(date__year=date.year,
                                       date__month=date.month)
 
    return render(response, "main/home.html", {"formC": formC, "formD":formD, "debitData": debitData, "creditData": creditData})

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
            except IntegrityError:
                messages.info(response, "Account already exists")
            
        return redirect("/accounts")
    else:
        # returns a form for creating new account data
        form = CreateNewAccount()

    return render(response, "main/accounts.html", {"form": form})

# deleting data from credit or debit table
@login_required(login_url="/login/")
def delete(response, id):
    
    # delete transaction
    try:
        if "debit" in response.POST:
            debit = Debit.objects.get(id=id)
            debit.delete()
        elif "credit" in response.POST:
            credit = Credit.objects.get(id=id)
            credit.delete()
    except ObjectDoesNotExist:
        print("test")

    return redirect("/")