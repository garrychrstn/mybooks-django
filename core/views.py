from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import date, timezone, datetime
from .forms import *
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
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
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            an = form.cleaned_data['author_nationality']
            am = form.cleaned_data['author_medsos']
            
            try:
                exist = user.books_set.get(title=title)
                messages.error(request, "Book with the same title already exist")
                return HttpResponseRedirect('/books/')

            except ObjectDoesNotExist:
                owner = user
                form.instance.owner = owner
                a = Archive(author=author, author_nationality=an, author_medsos=am, books=title)
                a.save()
                form.save()
                
                context = { 'user' : user, 'form' : form }
                messages.success(request, 'Library have been updated')
                return HttpResponseRedirect('/books/')

        else:
            context = { 'user' : user, 'form' : form }
            return render(request, 'user_books.html', context)
    
    else:
        form = AddBooks()
        context = { 'user' : user, 'form' : form }
        return render(request, 'user_books.html', context)    

@login_required
def library(request):
    user = request.user
    user_books = user.books_set.all()
    context = {
        'user' : user,
        'user_books' : user_books
    }
    return render(request, 'user_library.html', context)

@login_required
def update_library(request, id):
    user = request.user
    book = Books.objects.get(pk=id)
    print(f"{book.title}")
    notes = book.notes_set.all().order_by('-volume')
    if request.method == 'POST':
        form = UpdateBooks(request.POST)
        if form.is_valid():
            form.instance.books = book
            form.save()
        
        context = {
            'form' : form,
            'book' : book,
            'notes' : notes,
        }
        messages.success(request, 'Library have been updated')
        return render(request, 'user_update.html', context)
    else:
        form = UpdateBooks()
        return render(request, 'user_update.html', {'form' : form, 'book' : book, 'notes' : notes})
    
# BELOW IS FOR FORM TYPE LIBRARY
# @login_required
# def update_library(request):
#     user = request.user

#     if request.method == 'POST':
#         book_id = request.POST.get('book_id')
#         print(f"book id : {book_id}")
#         # book = user.books_set.get(pk=book_id)
#         if book_id is not None:  
#             book = get_object_or_404(user.books_set, pk=book_id)
#             form = UpdateBooks(request.POST)
#             if form.is_valid():
#                 thebook = book
#                 form.instance.book = thebook
#                 form.save()

#         context = {
#             # 'book_id' : book_id,
#             'book' : book,
#             'form' : form
#         }
#         messages.success(request, 'Library have been updated')
#         # return HttpResponseRedirect('/library/update/')
#         return render(request, 'user_update.html', context)
#     else :
#         context = {
#             # 'book_id' : book_id,
#             'book' : book
#         }
#         return render(request, 'user_update.html', context)


@login_required
def profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = SetProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        
        return render(request, 'user_profile.html')
    else:
        form = SetProfile(instance=profile)
                
    context = { 
        'user' : user, 
        'profile' : profile,
        'form' : form
    }
    return render(request, 'user_profile.html', context)
def signup(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            form.save()
            # after the registration is complete, create a profile set
            user = User.objects.get(username=username)
            user.profile_set.create()
            # automatically login after registration and profile set up complete
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are logged as {username}")
                return redirect("core:index")
            else:
                messages.error(request, "Invalid username or password")
        
            context = { 'form' : form }
            return redirect('/login/')

    else:
        form = RegisterForm()
        
    return render(request, 'signup.html', { 'form' : form })


def success(response):
    return render(response, 'success.html')