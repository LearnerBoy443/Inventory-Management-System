import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Product, Category, Transaction, User
from .forms import CustomUserCreationForm, LoginForm

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def products(request):
    return render(request, 'products.html')

@login_required
def categories(request):
    return render(request, 'categories.html')

@login_required
def edit_product(request, pid):
    return render(request, 'edit_product.html', {'pid': pid})

# Auth views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
