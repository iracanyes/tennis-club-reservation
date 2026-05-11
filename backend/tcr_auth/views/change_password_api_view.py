from rest_framework import permissions, status
from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tcr_auth.serializers import ChangePasswordSerializer


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        if request.user.is_active:
            print(f"ChangePasswordAPIView request.user : {request.user} {request.user.firstname} {request.user.lastname} {request.user.aft_id}")

            request.data["aft_id"] = request.user.aft_id

            print(f"ChangePasswordAPIView request.data['aft_id'] : {request.data["aft_id"]}")

            serializer = ChangePasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            member = serializer.validated_data["member"]
            confirm_new_password = serializer.validated_data["confirm_new_password"]

            member.set_password(confirm_new_password)

            member.save()

            return Response(status=status.HTTP_201_CREATED, data={"message" : "Password change successful!"})

        raise NotAuthenticated(detail="Unauthorized")
