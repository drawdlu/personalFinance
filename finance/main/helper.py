from .models import Accounts, Category

# returns a dict of all values from form
def get_values(form_data):
    # create dict for holding the form data values
    data = dict.fromkeys(['amount','description', 'date', 'account', 'category'])
    
    # extract values
    amount = form_data.cleaned_data["amount"]
    description = form_data.cleaned_data["description"]
    date = form_data.cleaned_data["date"]
    acc = form_data.cleaned_data["account"]
    ca = form_data.cleaned_data["category"]
    account = Accounts.objects.get(account_name=acc)
    category = Category.objects.get(category_name=ca)

    # save values to dict and return
    data["amount"] = amount
    data["description"] = description
    data["date"] = date
    data["account"] = account
    data["category"] = category

    return data

