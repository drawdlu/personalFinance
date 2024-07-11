from django.shortcuts import render, redirect
from .models import Accounts, Category, Debit, Credit
from .forms import CreateNewAccount, CreateNewCategory, CreateNewEntry, EditAccount, EditCategory, ChooseDate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .helper import get_values, get_summary
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# main page showing current months balance sheet
@login_required(login_url="/login/")
def home(response):
    userAccounts = response.user.accounts
    userCategories = response.user.category
    userDebit = response.user.debit
    userCredit = response.user.credit

    if response.method == "POST":
        formC = CreateNewCategory(response.POST)
        formD = CreateNewEntry(response.POST)

        # pressed add expense button
        if "add_expense" in response.POST:
            # gate data from form and save it 
            if formD.is_valid():
                data = get_values(response, formD)
                new = Debit(amount=-data["amount"], description=data["description"], account=data["account"], category=data["category"], date=data["date"])
                new.save()

                # create debit
                userDebit.add(new)
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
                userCredit.add(new)
            else:
                print("not valid expense")

        # update account
        try:
            account = userAccounts.get(account_name=data["account"])
            account.balance += new.amount
            account.save()
        except UnboundLocalError:
            messages.info(response, "Bill Gates?")
                
        return redirect("/")
    
    else:
        # create forms for user
        formC = CreateNewCategory()
        formD = CreateNewEntry()
        # make sure forms contains only categories and accounts of current user
        formD.fields["category"].queryset = userCategories.all()
        formD.fields["account"].queryset = userAccounts.all()

    # filter and return current months debit and credit
    date = datetime.now()
    debitData = userDebit.filter(date__year=date.year,
                                     date__month=date.month)
    creditData = userCredit.filter(date__year=date.year,
                                       date__month=date.month)
    
    # get totals using summary, index 0 is for overall total and index 1 is dict of total for each category
    # get total of each category in credit
    creditSummary = get_summary(creditData)
    creditCategory = creditSummary[1]
    creditTotal = creditSummary[0]

    # get total of each category in debit
    debitSummary = get_summary(debitData)
    debitCategory = debitSummary[1]
    debitTotal = debitSummary[0]
    print(debitTotal)

    return render(response, "main/home.html", {"formC": formC, "formD":formD, "debitData": debitData, "creditData": creditData, "debitCategory": debitCategory, "creditCategory": creditCategory, "debitTotal": debitTotal, "creditTotal": creditTotal})

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
def delete(response, id):
    userAccounts = response.user.accounts
    # updates account balance then deletes transaction based on the button pressed
    try:
        if "debit" in response.POST:
            # get transaction object
            debit = Debit.objects.get(id=id)
            # update balance
            userAccounts = userAccounts.get(account_name=debit.account)
            userAccounts.balance += abs(debit.amount)
            userAccounts.save()
            # delete transaction
            debit.delete()

        elif "credit" in response.POST:
            # get transaction object
            credit = Credit.objects.get(id=id)
            # update balance
            userAccounts = userAccounts.get(account_name=credit.account)
            userAccounts.balance -= credit.amount
            userAccounts.save()
            # delete transaction
            credit.delete()


    except ObjectDoesNotExist:
        print("Object does not exist")

    # redirect to current page user is on
    return redirect(response.META.get('HTTP_REFERER'))

# for displaying history of transaction per month based on user input
@login_required(login_url="/login/")
def history(response):
    userDates = response.user.monthyear
    userCredit = response.user.credit
    userDebit = response.user.debit

    if response.method == "POST":
        form = ChooseDate(userDates.all(), response.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]

            # save date into a datetime format
            date = datetime.strptime(date, '%Y-%m-%d').date()

            # filter dates
            debitData = userDebit.filter(date__year=date.year,
                                    date__month=date.month)
            
            creditData = userCredit.filter(date__year=date.year,
                                                      date__month=date.month)

            # get totals using summary, index 0 is for overall total and index 1 is dict of total for each category
            # get total of each category in credit
            creditSummary = get_summary(creditData)
            creditCategory = creditSummary[1]
            creditTotal = creditSummary[0]

            # get total of each category in debit
            debitSummary = get_summary(debitData)
            debitCategory = debitSummary[1]
            debitTotal = debitSummary[0]

            # for checking whether to display tables
            posted = True

    else:
        posted = False
        debitData = None
        creditData = None
        creditCategory = None
        debitCategory = None
        creditTotal = 0
        debitTotal = 0
        form = ChooseDate(userDates.all())

    return render(response, "main/history.html", {"form": form, "debitData": debitData, "creditData": creditData, "creditCategory": creditCategory, "debitCategory": debitCategory, "creditTotal": creditTotal, "debitTotal": debitTotal, "posted": posted})