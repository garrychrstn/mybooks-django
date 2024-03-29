"""MyBooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('library/', views.library, name='library'),
    path('books/', views.books, name='books'),
    path('success/', views.success, name='success'),
    path('library/update/<int:id>', views.update_library, name='update_library'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)