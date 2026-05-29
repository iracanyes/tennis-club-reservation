import logging
from rest_framework import viewsets, permissions
from reservations.models import Court
from reservations.serializers import CourtSerializer


class CourtViewSet(viewsets.ModelViewSet):
    queryset = Court.objects.all().order_by('-number')
    serializer_class = CourtSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]

        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]