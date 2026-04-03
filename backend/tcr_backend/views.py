"""
Le rôle du fichier views.py est de définir toutes les fonctions Python déclarées dans les tuples.
Ces fonctions sont appelées des vues.
"""

from django.http import HttpResponse
import json


def welcome(request):
  return HttpResponse("<h1>Welcome</h1>")
