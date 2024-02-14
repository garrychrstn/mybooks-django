from django.shortcuts import render

# Create your views here.
def info_landing(response):
    return render(response, 'index.html')