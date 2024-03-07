from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import date, timezone, datetime
from .forms import *
from django.db.models import Prefetch, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from . forms import *
from . models import *
import random
# Create your views here.

def index(response):
    user = None
    if response.user.is_authenticated:
        user = response.user
        pref_array = user.profile.preference.split(",") # Create array from preference so it can be used with for loop
        prefs = [x.strip(' ') for x in pref_array]
        queries = [Q(genre__contains=pref) for pref in pref_array]

        combined_pref = queries[0]
        for query in queries[1::]:
            combined_pref != query
        
        filtered_queryset = Library.objects.filter(combined_pref)[:5]
        print(f"Prefs : {prefs}\n")
        print(f"Queries : {queries}\n")
        print(f"Combined Pref: {combined_pref}\n")
        print(f"Filtered Query : {filtered_queryset}")
    return render(response, 'index.html', {'user' : user, 'pref_array' : pref_array, 'filtered_queryset' : filtered_queryset})

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
def addBook(request):
    user = request.user
    p = Profile.objects.get(username=user.id)

    if request.method == 'POST':
        form = AddBook(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data['title']

            print(f"errc : {title}")
            try:
                Library.objects.filter(title=title).exists() # Check whether book has already added to Library, if YES then tie the book to user
                book = Library.objects.get(title=title)
                book.profile.add(p)
                Note(profile=p, book=book)
            except ObjectDoesNotExist: # If book doesn't exist in Library, create a new instance of book then tie it to the user.
                form.save()
                b = Library.objects.get(title=title)
                b.profile.add(p)
                Note(profile=p, book=book)
                                       
            context = { 'user' : user, 'form' : form }
            messages.success(request, 'Library have been updated')
            return HttpResponseRedirect('/books/')

        else:
            context = { 'user' : user, 'form' : form }
            return render(request, 'user_books.html', context)
    
    else:
        form = AddBook()
        context = { 'user' : user, 'form' : form }
        return render(request, 'user_books.html', context)    

@login_required
def library(request):
    user = request.user
    p = Profile.objects.get(username=user.id)
    user_book = p.library_set.all()
    print(user_book)
    context = {
        'user' : user,
        'user_book' : user_book
    }
    return render(request, 'user_library.html', context)

@login_required
def update_library(request, id):
    user = request.user
    pr = Profile.objects.get(username=user.id)
    book = Library.objects.get(pk=id)
    print(f"{book} and {pr}")
    # update = Note.objects.get(book=book.id, profile=pr.id)

    print(f"{book.title}")
    notes = book.note_set.all().order_by('-volume')
    if request.method == 'POST':
        form = UpdateBook(request.POST)
        if form.is_valid():
            form.instance.book = book
            form.instance.profile = pr
            form.save()
        
        context = {
            'form' : form,
            'book' : book,
            'notes' : notes,
        }
        spread_score = book.note_set.values('rate')
        current_score = 0
        for score in spread_score:
            current_score += score['rate']
        
        book.update(score=current_score)
        messages.success(request, 'Library have been updated')
        return render(request, 'user_update.html', context)
    else:
        form = UpdateBook()
        return render(request, 'user_update.html', {'form' : form, 'book' : book, 'notes' : notes})
    
# BELOW IS FOR FORM TYPE LIBRARY
# @login_required
# def update_library(request):
#     user = request.user

#     if request.method == 'POST':
#         book_id = request.POST.get('book_id')
#         print(f"book id : {book_id}")
#         # book = user.book_set.get(pk=book_id)
#         if book_id is not None:  
#             book = get_object_or_404(user.book_set, pk=book_id)
#             form = UpdateBook(request.POST)
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