import logging

from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from reservations.models import Court
from reservations.serializers import CourtSerializer


class CourtViewSet(viewsets.ModelViewSet):
    __logger = logging.getLogger(__name__)
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

    def create(self, request):
        if settings.DEBUG :
            self.__logger.warning(f"CourtViewSet.create - request.body : {request.body}")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save court,
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        if settings.DEBUG :
            self.__logger.warning(f"CourtViewSet.update - request.body : {request.body}")

        raise NotImplementedError("Court update not implemented!")

    def partial_update(self, request, *args, **kwargs):
        raise NotImplementedError("Court's partial update not implemented!")

    def destroy(self, request, pk=None):
        court = get_object_or_404(self.queryset, pk=pk)
        try:
            court.delete()
        except:
            raise APIException(detail="An error occured while deleting court.")

        return Response(status=status.HTTP_204_NO_CONTENT)