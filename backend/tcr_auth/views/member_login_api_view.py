from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tcr_auth.config import set_token_cookies
from members.serializers import MemberLoginSerializer

class MemberLoginAPIView(APIView):
    permission_classes = []

    def post(self, request):

        print(f"MemberLoginView post request.data : {request.data}")

        serializer = MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = serializer.validated_data['member']

        # Create auth token & refresh token
        refresh = RefreshToken.for_user(member)

        response = Response(status=status.HTTP_200_OK, data= {'token' : str(refresh.access_token), 'type' : 'member'})



        # Set token on HTTP only cookies
        set_token_cookies(response, str(refresh.access_token), str(refresh))

        return response