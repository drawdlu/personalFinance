from django.shortcuts import render, redirect
from .models import Accounts, Category, Debit, Credit
from .forms import CreateNewAccount, CreateNewCategory, CreateNewEntry, EditAccount, EditCategory
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .helper import get_values
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# main page showing current months balance sheet
@login_required(login_url="/login/")
def home(response):
    if response.method == "POST":
        formC = CreateNewCategory(response.POST)
        formD = CreateNewEntry(response.POST)

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
    debitData = response.user.debit.filter(date__year=date.year,
                                     date__month=date.month)
    creditData = response.user.credit.filter(date__year=date.year,
                                       date__month=date.month)
 
    return render(response, "main/home.html", {"formC": formC, "formD":formD, "debitData": debitData, "creditData": creditData})

# creating new accounts and showing account data
@login_required(login_url="/login/")
def accounts(response):
    userAccounts = response.user.accounts
    userCategories = response.user.category

    # user clicked ADD ACCOUNT
    if response.method == "POST":
        # add account button pressed
        if "addAccount" in response.POST:
            formA = CreateNewAccount(response.POST)
            # try to create a new account
            if formA.is_valid():
                n = formA.cleaned_data["account_name"].upper()
                b = formA.cleaned_data["balance"]
                new = Accounts(account_name=n, balance=b)
                new.save()

                # create account
                try:
                    userAccounts.add(new)
                # catch duplicates
                except IntegrityError:
                    messages.info(response, "Account already exists")
                
            return redirect("/accounts")
        
        # add category button pressed
        elif "addCategory" in response.POST:
            formC = CreateNewCategory(response.POST)
            if formC.is_valid():
                n = formC.cleaned_data["category_name"].upper()
                new = Category(category_name=n)
                new.save()
            # create category
            try:
                userCategories.add(new)
            except IntegrityError:
                messages.info(response, "Category already exists.")

        # edit account button pressed
        elif "editAccount" in response.POST:
            formEditA = EditAccount(userAccounts.all(), response.POST)
            if formEditA.is_valid():
                name = formEditA.cleaned_data["name"]
                newName = formEditA.cleaned_data["newName"]
                newBalance = formEditA.cleaned_data["newBalance"]
                account = userAccounts.get(account_name=name)

                # if name is input, update name
                if newName:
                    account.account_name = newName.upper()
                
                # if balance is input, update balance
                if newBalance:
                    account.balance = newBalance
                
                # catch user updating to account names that already exist
                try:
                    account.save()
                except IntegrityError:
                    messages.info(response, "Account with that name already exists")

        # edit category button pressed
        elif "editCategory" in response.POST:
            formEditC = EditCategory(userCategories.all(), response.POST)
            if formEditC.is_valid():
                name = formEditC.cleaned_data["name"]
                newName = formEditC.cleaned_data["newName"]
                category = userCategories.get(category_name=name)

                # update name only if input is given
                if newName:
                    category.category_name = newName.upper()
                
                # catch names that already exists in users categories
                try:
                    category.save()
                except IntegrityError:
                    messages.info(response, "Category with that name already exists")
            
        return redirect("/accounts")
    else:
        # returns a form for creating new account data
        formA = CreateNewAccount()
        formC = CreateNewCategory()
        formEditA = EditAccount(userAccounts.all())
        formEditC = EditCategory(userCategories.all())

    return render(response, "main/accounts.html", {"formA": formA, "formC": formC, "formEditA": formEditA, "formEditC": formEditC})

# deleting data from credit or debit table
@login_required(login_url="/login/")
def edit(response, id):
    
    # delete transaction
    try:
        if "debit" in response.POST:
            debit = Debit.objects.get(id=id)
            debit.delete()
        elif "credit" in response.POST:
            credit = Credit.objects.get(id=id)
            credit.delete()
    except ObjectDoesNotExist:
        print("Object does not exist")

    return redirect("/")