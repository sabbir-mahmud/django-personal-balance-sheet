# imports
from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expenses', views.all_expenses, name='expenses'),
    path('expenses/edit/<str:pk>', views.edit_expense, name='edit_expense'),
    path('expenses/<str:pk>', views.delete_expense, name='delete_expenses'),
    path('incomes', views.all_incomes, name='incomes'),
    path('incomes/edit/<str:pk>', views.edit_income, name='edit_income'),
    path('incomes/<str:pk>', views.delete_income, name='delete_income'),
    path('months', views.months, name='months'),
    path('months/<str:pk>', views.edit_months, name='edit_months'),
    path('years', views.years, name='years'),
    path('years/<str:pk>', views.edit_years, name='edit_years'),
]
