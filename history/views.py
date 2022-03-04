# imports
from django.shortcuts import render, redirect
from .models import Month, Year, Income, Expense
from .forms import MonthForm, YearForm, IncomeForm, ExpenseForm
from django.db.models import Sum
from django.db.models import Q
from django.core.paginator import Paginator
from .signals import active_date, active_year
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.

# dashboard view

@login_required(login_url='login')
def dashboard(request):
    # dynamic active month and year
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    active_date(month)
    active_year(year)
    actived_month = Month.objects.get(active=True)
    actived_year = Year.objects.get(active=True)
    # get user
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    prev_monthly_expense = 0
    prev_id = actived_month.id - 1
    prev_month = Month.objects.filter(id=prev_id).first()
    if Expense.objects.filter(Q(user=user) & Q(month=prev_month) & Q(year__active=True)):
        prev_monthly_expense = Expense.objects.filter(Q(user=user) & Q(month=prev_month) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']
        print(prev_monthly_expense)

    prev_monthly_income = 0
    if Income.objects.filter(Q(user=user) & Q(month=prev_month) & Q(year__active=True)):
        prev_monthly_income = Income.objects.filter(Q(user=user) & Q(month=prev_month) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense

    earns = Income.objects.filter(Q(user=user) & Q(
        month__active=True)).order_by('-id')[:5]
    expenses = Expense.objects.filter(
        Q(user=user) & Q(month__active=True)).order_by('-id')[:5]

    # form data for add income and expense
    income_form = IncomeForm(
        initial={'user': user, 'month': actived_month, 'year': actived_year})
    expense_form = ExpenseForm(
        initial={'user': user, 'month': actived_month, 'year': actived_year})
    if request.method == 'POST':
        if 'income_details' in request.POST:
            income_form = IncomeForm(request.POST, initial={'user': user})
            if income_form.is_valid():
                income_form.save()
                return redirect('dashboard')
        elif 'expense_details' in request.POST:
            expense_form = ExpenseForm(request.POST, initial={'user': user})
            if expense_form.is_valid():
                expense_form.save()
                return redirect('dashboard')

    context = {
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'prev_monthly_expense': prev_monthly_expense,
        'balance': balance,
        'earns': earns,
        'expenses': expenses,
        'income_form': income_form,
        'expense_form': expense_form,
        'prev_monthly_income': prev_monthly_income,
    }
    return render(request, 'history/dashboard.html', context)

# all expenses view


@login_required(login_url='login')
def all_expenses(request):
    actived_month = Month.objects.get(active=True)
    actived_year = Year.objects.get(active=True)
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    expenses = Expense.objects.filter(user=user).order_by('-id')
    p = Paginator(expenses, 15)
    page = request.GET.get('p')
    expenses = p.get_page(page)
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense_form.save()
            return redirect('expenses')
    else:
        expense_form = ExpenseForm(
            initial={'user': user, 'month': actived_month, 'year': actived_year})

    context = {
        'expenses': expenses,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
        'expense_form': expense_form,
    }
    return render(request, 'history/all_expenses.html', context)

# edit expense view


@login_required(login_url='login')
def edit_expense(request, pk):
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    expense = Expense.objects.get(pk=pk)
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST, instance=expense)
        if expense_form.is_valid():
            expense_form.save()
            return redirect('expenses')
    else:
        expense_form = ExpenseForm(instance=expense)
    context = {
        'form': expense_form,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,

    }
    return render(request, 'history/edit_invoice.html', context)


@login_required(login_url='login')
def delete_expense(request, pk):
    expense = Expense.objects.get(pk=pk)
    expense.delete()
    return redirect('expenses')


# all income view

@login_required(login_url='login')
def all_incomes(request):
    actived_month = Month.objects.get(active=True)
    actived_year = Year.objects.get(active=True)
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    earns = Income.objects.filter(user=user).order_by('-id')
    p = Paginator(earns, 15)
    page = request.GET.get('page')
    earns = p.get_page(page)
    if request.method == 'POST':
        income_form = IncomeForm(request.POST, initial={'user': user})
        if income_form.is_valid():
            income_form.save()
            return redirect('incomes')
    else:
        income_form = IncomeForm(
            initial={'user': user, 'month': actived_month, 'year': actived_year})

    context = {
        'earns': earns,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
        'income_form': income_form,
    }
    return render(request, 'history/all_incomes.html', context)

# edit income view


@login_required(login_url='login')
def edit_income(request, pk):
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    income = Income.objects.get(pk=pk)
    if request.method == 'POST':
        income_form = IncomeForm(request.POST, instance=income)
        if income_form.is_valid():
            income_form.save()
            return redirect('incomes')
    else:
        form = IncomeForm(instance=income)
    context = {
        'form': form,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,

    }
    return render(request, 'history/edit_invoice.html', context)

# delete income view


@login_required(login_url='login')
def delete_income(request, pk):
    income = Income.objects.get(pk=pk)
    income.delete()
    return redirect('incomes')


# month view
@login_required(login_url='login')
def months(request):
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    months = Month.objects.all().order_by('-id')
    p = Paginator(months, 15)
    page = request.GET.get('page')
    months = p.get_page(page)

    forms = MonthForm()
    if request.method == 'POST':
        forms = MonthForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('months')
    context = {
        'months': months,
        'forms': forms,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
    }
    return render(request, 'history/months.html', context)


# month edit view
@login_required(login_url='login')
def edit_months(request, pk):
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    month = Month.objects.filter(id=pk).first()
    months = Month.objects.all().order_by('-id')
    p = Paginator(months, 15)
    page = request.GET.get('page')
    months = p.get_page(page)

    forms = MonthForm(instance=month)
    if request.method == 'POST':
        forms = MonthForm(request.POST, instance=month)
        if forms.is_valid():
            forms.save()
            return redirect('months')
    context = {
        'months': months,
        'forms': forms,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
    }
    return render(request, 'history/months.html', context)

# month view


@login_required(login_url='login')
def years(request):
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    years = Year.objects.all().order_by('-id')
    p = Paginator(years, 15)
    page = request.GET.get('page')
    years = p.get_page(page)

    forms = YearForm()
    if request.method == 'POST':
        forms = YearForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('years')
    context = {
        'years': years,
        'forms': forms,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
    }
    return render(request, 'history/years.html', context)


# month edit view
@login_required(login_url='login')
def edit_years(request, pk):
    user = request.user
    total_earn = 0
    if Income.objects.filter(user=user):
        total_earn = Income.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_earn = 0
    if Income.objects.filter(Q(month__active=True) & Q(
            year__active=True)):
        monthly_earn = Income.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    total_expense = 0
    if Expense.objects.filter(user=user):
        total_expense = Expense.objects.filter(
            user=user).aggregate(Sum('amount'))['amount__sum']

    monthly_expense = 0
    if Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)):
        monthly_expense = Expense.objects.filter(Q(user=user) & Q(month__active=True) & Q(
            year__active=True)).aggregate(Sum('amount'))['amount__sum']

    balance = total_earn - total_expense
    year = Year.objects.filter(id=pk).first()
    years = Month.objects.all().order_by('-id')
    p = Paginator(years, 15)
    page = request.GET.get('page')
    years = p.get_page(page)

    forms = YearForm(instance=year)
    if request.method == 'POST':
        forms = YearForm(request.POST, instance=year)
        if forms.is_valid():
            forms.save()
            return redirect('years')
    context = {
        'years': years,
        'forms': forms,
        'total_earn': total_earn,
        'monthly_earn': monthly_earn,
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'balance': balance,
    }
    return render(request, 'history/years.html', context)
