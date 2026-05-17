from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from tcr_auth.config import set_token_cookies
from tcr_auth.serializers import AdminLoginGoogleSerializer


class AdminLoginGoogleAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):

        serializer = AdminLoginGoogleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admin = serializer.validated_data['admin']


        # Create auth token & refresh token
        refresh = RefreshToken.for_user(admin)

        response = Response(status=status.HTTP_200_OK, data={'token': str(refresh.access_token), 'type': 'admin'})

        # Set token on HTTP only cookies
        set_token_cookies(response, str(refresh.access_token), str(refresh))

        return response
        