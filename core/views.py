from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import date, timezone, datetime
from .forms import *
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . forms import *
from . models import *

# Create your views here.

def index(response):
    username = None
    if response.user.is_authenticated:
        username = response.user.username
    return render(response, 'index.html', {'username' : username})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are logged as {username}")
                return redirect("core:index")
            else:
                messages.error(request, "Invalid username or password")
            
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form' : form})            

@login_required
def books(request):
    user = request.user
    
    if request.method == 'POST':
        form = AddBooks(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            tl_type = form.cleaned_data['tl_type']
            series_status = form.cleaned_data['series_status']
            source = form.cleaned_data['source']
            reading_status = form.cleaned_data['reading_status']
            current_progress = form.cleaned_data['current_progress']
        
        user.books_set.create(title=title, author=author, tl_type=tl_type, series_status=series_status, source=source, reading_status=reading_status, current_progress=current_progress)
        user.save()
        context = { 'user' : user, 'form' : form }
        return render(request, 'books.html', context)
    
    else:
        form = AddBooks()
        context = { 'user' : user, 'form' : form }
    return render(request, 'books.html', context)    

def profile(request):
    pass