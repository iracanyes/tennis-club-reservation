from datetime import datetime

from django.shortcuts import render

def login(request):
  return render(request,'login.html', {'current_date_time' : datetime.now})