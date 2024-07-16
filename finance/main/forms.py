from django import forms
from .models import Category, Debit, Accounts, MonthYear

# for creating new accounts
class CreateNewAccount(forms.ModelForm):
    class Meta:
        model = Accounts
        exclude = ['user']

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

# for editing accounts
class EditAccount(forms.Form):
    def __init__(self, accountList, *args, **kwargs):
        super(EditAccount, self).__init__(*args, **kwargs)
        if accountList:
            namesA = (('', '-----------'),)
            namesB = tuple([(name, name) for name in accountList])
            allNames = namesA + namesB
            self.fields['name'] = forms.ChoiceField(choices=allNames, initial=None)
        else:
            self.fields['name'] = forms.ChoiceField(label="No Accounts Yet", disabled=True)
    
    name = forms.ChoiceField()
    newName = forms.CharField(max_length=200, label="Edit Name", required=False)
    newBalance = forms.DecimalField(max_digits=13, decimal_places=2, label="Edit Balance", required=False)

# for editing accounts
class EditCategory(forms.Form):
    def __init__(self, categoryList, *args, **kwargs):
        super(EditCategory, self).__init__(*args, **kwargs)
        if categoryList:
            namesA = (('', '-----------'),)
            namesB = tuple([(name, name) for name in categoryList])
            allNames = namesA + namesB
            self.fields['name'] = forms.ChoiceField(choices=allNames, initial=None)
        else:
            self.fields['name'] = forms.ChoiceField(label="No Categories Yet", disabled=True)
    
    name = forms.ChoiceField()
    newName = forms.CharField(max_length=200, label="Edit Name")

# for choosing which history to display
class ChooseDate(forms.Form):
    def __init__(self, dateList, *args, **kwargs):
        super(ChooseDate, self).__init__(*args, **kwargs)
        if dateList:
            datesA = tuple([(date.date.strftime('%Y-%m-%d'), date.date.strftime('%m-%Y')) for date in dateList])
            datesB = (('', '-----------'),)
            allDates = datesB + datesA
            self.fields['date'] = forms.ChoiceField(choices=allDates, initial=None)
        else:
            self.fields['date'] = forms.ChoiceField(label="No Transactions Yet", disabled=True)
    
    date = forms.ChoiceField()

