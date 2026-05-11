from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView


class CRSFApiView(APIView):
    permission_classes = []
    authentication_classes = []


    def get(self, request):
        token = get_token(request)

        print(f"CSRFApiview get - token : {token}")

        return Response({ "csrf_token" : token })