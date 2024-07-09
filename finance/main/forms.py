from django import forms
from .models import Category, Debit, Accounts

# for creating new accounts
class CreateNewAccount(forms.Form):
    name = forms.CharField(label="Account Name: ", max_length=200)
    balance = forms.DecimalField(max_digits=13)

# for creating new categories
class CreateNewCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]

# custom widget for inputting date
class DateInput(forms.DateInput):
    input_type = 'date'

# for adding expenses
class CreateNewEntry(forms.ModelForm):
    class Meta: 
        model = Debit
        fields = ["date", "amount", "description", "account", "category"]
        widgets = {
            'date': DateInput()
        }