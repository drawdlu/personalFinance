from django.contrib import admin
from .models import Accounts, Category, Debit, Credit, MonthYear

# Register your models here.
admin.site.register(Accounts)
admin.site.register(Category)
admin.site.register(Debit)
admin.site.register(Credit)
admin.site.register(MonthYear)