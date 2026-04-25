from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from administrators.serializers import AdminLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from tcr_auth.config import set_token_cookies


class AdminLoginAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admin = serializer.validated_data['admin']

        # Create Token & Refresh token
        refresh = RefreshToken.for_user(admin)

        response = Response({'status':status.HTTP_200_OK, 'data': {'token' : str(refresh.access_token), 'refresh_token' : str(refresh), 'type' : 'admin'}})

        # Set token on HTTP only cookies
        set_token_cookies(response, str(refresh.access_token), str(refresh))

        return response


