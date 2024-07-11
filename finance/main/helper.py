from datetime import datetime
from .models import MonthYear
from django.db import IntegrityError

# returns a dict of all values from form
def get_values(response, form_data):
    # create dict for holding the form data values
    data = dict.fromkeys(['amount','description', 'date', 'account', 'category'])
    
    # extract values from form
    amount = abs(form_data.cleaned_data["amount"])
    description = form_data.cleaned_data["description"]
    acc = form_data.cleaned_data["account"]
    ca = form_data.cleaned_data["category"]
    account = response.user.accounts.get(account_name=acc)
    category = response.user.category.get(category_name=ca)
    date = form_data.cleaned_data["date"]

    # get first day of month date for transaction month and year storage
    n = datetime(date.year, date.month, 1).date()
    new = MonthYear(date=n)
    new.save()

    try:
        response.user.monthyear.add(new)
    except IntegrityError:
        print("month-year already saved")

    # save values to dict and return
    data["amount"] = amount
    data["description"] = description
    data["date"] = date
    data["account"] = account
    data["category"] = category

    return data

def get_summary(transactions):
    categoryTotals = {}
    total = 0

    for transaction in transactions:
        if transaction.category not in categoryTotals:
            categoryTotals[transaction.category] = transaction.amount
        else:
            categoryTotals[transaction.category] += transaction.amount
        total += transaction.amount

    return [total, categoryTotals]
