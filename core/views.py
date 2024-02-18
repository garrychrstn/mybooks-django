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
    user = None
    if response.user.is_authenticated:
        user = response.user
    return render(response, 'index.html', {'user' : user})

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
        form = AddBooks(request.POST, request.FILES)
        
        if form.is_valid():
            # title = form.cleaned_data['title']
            # author = form.cleaned_data['author']
            # author_nationality = form.cleaned_data['author_nationality']
            # author_medsos = form.cleaned_data['author_medsos']
            # book_type = form.cleaned_data['book_type']
            # tl_type = form.cleaned_data['tl_type']
            # series_status = form.cleaned_data['series_status']
            # source = form.cleaned_data['source']
            # reading_status = form.cleaned_data['reading_status']
            # current_progress = form.cleaned_data['current_progress']
            # cover = form.files['cover']
            # if cover:
            #     cover.save(f"cover/{user.username}/{title}/{cover.name}")

            # user.books_set.create(title=title, author=author, author_nationality=author_nationality, author_medsos=author_medsos, book_type=book_type, tl_type=tl_type, series_status=series_status, source=source, reading_status=reading_status, current_progress=current_progress, cover=cover.name)
            owner = user
            form.instance.owner = owner
            form.save()
            
            context = { 'user' : user, 'form' : form }
            messages.success(request, 'Library have been updated')
            return HttpResponseRedirect('/books/')
        else:
            context = { 'user' : user, 'form' : form }
            return render(request, 'books.html', context)
    
    else:
        form = AddBooks()
        context = { 'user' : user, 'form' : form }
        return render(request, 'books.html', context)    

def profile(request):
    pass

def success(response):
    return render(response, 'success.html')