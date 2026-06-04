from django.http import QueryDict
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from reservations.models import Reservation
from reservations.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().filter(event_type=Reservation.EventTypeChoices.EVENT)
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        permission_classes = []
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]

        if self.action == "create" or self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        List all events
        """
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        """
        Create a new event
        """
        # Enable mutability on immutable QueryDict
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        # Member can only author their reservation
        # Set authenticated member as reservation's author
        request.data["author_id"] = str(request.user.id)
        request.data["status"] = Reservation.StatusChoices.ACTIVE

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)