from django.db import models
from django.contrib.auth.models import User


# tracking user accounts
class Accounts(models.Model):
    user = models.ForeignKey(User, related_name="accounts", null=True, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return self.account_name
    
    # make account_name unique only to the current user
    class Meta:
        unique_together = 'user', 'account_name'

# category of expenses
class Category(models.Model):
    user = models.ForeignKey(User, related_name="category", null=True, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name
    
    # make account_name unique only to the current user
    class Meta:
        unique_together = 'user', 'category_name'

# tracking user expenses / debit
class Debit(models.Model):
    user = models.ForeignKey(User, related_name="debit", null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    account = models.ForeignKey(Accounts, related_name="acc", null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name="cat", null=True, on_delete=models.PROTECT)

# tracking user earnings / credit
class Credit(models.Model):
    user = models.ForeignKey(User, related_name="credit", null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    account = models.ForeignKey(Accounts, related_name="accCredit", null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name="catCredit", null=True, on_delete=models.PROTECT)     

# track months and years with transactions
class MonthYear(models.Model):
    user = models.ForeignKey(User, related_name="monthyear", null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)

    # make monthYear unique only to the current user 
    class Meta:
        unique_together = 'user', 'date'