from django.contrib.auth.forms import AuthenticationForm
from django import forms

class MemberLoginForm(AuthenticationForm):
  username = forms.CharField(label="Numéro AFT")