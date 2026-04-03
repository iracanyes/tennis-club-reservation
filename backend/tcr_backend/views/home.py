from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def home(request):
  return render(request, 'home.html', {'current_date_time': datetime.now()})