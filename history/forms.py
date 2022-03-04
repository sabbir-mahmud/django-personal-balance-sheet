# imports
from cProfile import label
from django.forms import ModelForm
from .models import Month, Year, Income, Expense

# month form


class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = ['month', 'active']

# year form


class YearForm(ModelForm):
    class Meta:
        model = Year
        fields = ['year', 'active']

# income form


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['user', 'income_details', 'amount', 'month', 'year']


# expense form


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['user', 'expense_details', 'amount', 'month', 'year']
