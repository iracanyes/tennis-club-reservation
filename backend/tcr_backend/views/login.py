import os
from datetime import datetime
from django.shortcuts import render


def login(request):
  # Tester si les données du formulaire ont été envoyé
  if len(request.POST) > 0 :
    errors = {}
    # Test des paramètres attendus
    if 'aftId' not in request.POST:
      errors['aftId'] = 'AFT ID not provided'
    if 'password' not in request.POST:
      errors['password'] = 'Password not provided'
    # Retourner les erreurs
    if len(errors) > 0:
      return render(request,'login.html', {'current_date_time' : datetime.now, 'errors': errors})

    # Récupération des saisies
    aftId = request.POST['aftId']
    password = request.POST['password']

    # Validation des saisies

    # Si tout est OK, on redirige vers la page d'accueil
    return render(request, 'home.html', {'current_date_time' : datetime.now, 'aftId' : aftId })

  return render(request,'login.html', {'current_date_time' : datetime.now})