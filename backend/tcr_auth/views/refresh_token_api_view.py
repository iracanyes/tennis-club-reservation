from  django.conf import settings
from django.db.migrations import serializer
from rest_framework import status, response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import Token

from tcr_auth.config import set_token_cookies

class RefreshTokenAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data={ 'refresh': self.get_refresh_token_from_cookie() } )
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        response = Response({ 'message' : 'Authentication successfully!'}, status=status.HTTP_200_OK)

        access_token = serializer.validated_data.get('access')
        refresh_token = serializer.validated_data.get('refresh')

        set_token_cookies(response, access_token, refresh_token)

        return response


    def get_refresh_token_from_cookie(self):
        refresh = self.request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])

        if not refresh:
            raise PermissionDenied({ 'message': 'No refresh token provided.' })

        return refresh