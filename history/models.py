# imports
from django.db import models
from django.contrib.auth.models import User

# month model


class Month(models.Model):
    month = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.month

# year model


class Year(models.Model):
    year = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.year

# income model


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_details = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return self.income_details

# expense model


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_details = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return self.expense_details
