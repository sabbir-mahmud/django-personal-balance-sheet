# imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'moneybag/login.html')
