from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from members.serializers import MemberSerializer

class UserRetrieveAPIView(GenericAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user


    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)