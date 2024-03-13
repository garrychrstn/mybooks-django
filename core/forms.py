from django import forms
from . models import *
from . choices import *
from django.forms import inlineformset_factory, formset_factory, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



# class UserProfile(forms.ModelForm):
#     email = forms.EmailInput(
#         # required=True,
#     )
#     first_name = forms.CharField(
#         required=True,
#     )
#     last_name = forms.CharField(
#         required=True
#     )
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name']

# class SetProfile(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ['account_created', 'username']

# class AddBooks(forms.ModelForm):
#     class Meta:
#         model = Books
#         exclude = ["owner"]

# class UpdateBooks(forms.ModelForm):
#     class Meta:
#         model = Notes
#         exclude = ["books"]

# class RegisterForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']