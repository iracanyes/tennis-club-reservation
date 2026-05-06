from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from tcr_auth.config.jwt import delete_token_cookies


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenBlacklistSerializer

    def post(self, request):
        serializer = self.serializer_class(data={"refresh": self.get_refresh_token_from_cookie()})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        response = Response({},status=status.HTTP_200_OK)

        # Delete JWT cookies
        delete_token_cookies(response)

        return response

    def get_refresh_token_from_cookie(self):
        refresh = self.request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])

        print(f"LogoutAPIView.get_refresh_token_from_cookie: {refresh}")

        if not refresh:
            raise PermissionDenied

        return refresh
