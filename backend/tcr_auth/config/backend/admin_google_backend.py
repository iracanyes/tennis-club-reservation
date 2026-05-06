import os
from django.contrib.auth.backends import ModelBackend
from administrators.models import Admin
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.exceptions import ValidationError

class AdminGoogleBackend(ModelBackend):
    """
    Authenticate administrators with google account
    """
    def authenticate(self, request, token=None, **extra_fields):
        try:
            # La fonction verify_oauth2_token vérifie le jeton JWT signature, la revendication aud et la revendication exp.
            id_info = id_token.verify_token(token, requests.Request(), os.environ.get('GOOGLE_CLIENT_ID'))

            if id_info['aud'] not in [os.environ['GOOGLE_CLIENT_ID']]:
                raise ValueError("Could not verify audience.")

            admin = Admin.objects.get(email=id_info['email'])

            return admin
        except :
            return None