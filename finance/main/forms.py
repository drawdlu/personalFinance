from django import forms
from .models import Category

# for creating new accounts
class CreateNewAccount(forms.Form):
    name = forms.CharField(label="Account Name: ", max_length=200)
    balance = forms.DecimalField(max_digits=13)

# for creating new categories
class CreateNewCategory(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user']