from django.contrib import admin
from .models import Month, Year, Income, Expense

# Register your models here.
admin.site.register(Month)
admin.site.register(Year)
admin.site.register(Income)
admin.site.register(Expense)
