from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from members.models import Member
from members.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-date_joined')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):

        serializer = CategorySerializer(self.queryset, many=True)

        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = Member.objects.all()
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = CategorySerializer(category)

        return Response(serializer.data)