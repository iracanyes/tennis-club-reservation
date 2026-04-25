from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class AdminEmailLoginForm(AuthenticationForm):
  username = forms.CharField(label="Email")

