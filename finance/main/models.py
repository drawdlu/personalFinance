from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
