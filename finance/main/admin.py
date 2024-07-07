from django.contrib import admin
from .models import Accounts, Category, Debit

# Register your models here.
admin.site.register(Accounts)
admin.site.register(Category)
admin.site.register(Debit)