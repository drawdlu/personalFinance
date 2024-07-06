from django import forms

class CreateNewAccount(forms.Form):
    name = forms.CharField(label="Account Name: ", max_length=200)
    balance = forms.DecimalField(max_digits=13)