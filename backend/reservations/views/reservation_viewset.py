import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.db.migrations import serializer
from django.db.models.aggregates import Count
from django.http import QueryDict
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from members.models import Member
from reservations.permissions import IsAuthorOrAdminOrReadOnly
from reservations.models import Court, Reservation
from reservations.serializers import ReservationSerializer, ReservationDeleteSerializer, CourtReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    __logger = logging.getLogger(__name__)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdminOrReadOnly]

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        List all reservations
        """
        serializer = self.serializer_class(
            self.queryset.all(),
            many=True
        )

        return Response(serializer.data)


    def create(self, request):
        """
        Create a new reservation
        """
        if settings.DEBUG:
            self.__logger.warning(f"\nReservationViewSet.create() - request.body : \n{request.body} ")
            self.__logger.warning(f"\nReservationViewSet.create() - request.user :\n {request.user} ")


        # Enable mutability on immutable QueryDict
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        # Member can only author their reservation
        # Set authenticated member as reservation's author
        request.data["author_id"] = str(request.user.id)
        request.data["status"] = Reservation.StatusChoices.ACTIVE

        # Member are allowed to create only club reservations
        if not request.user.is_staff :
            request.data['event_type'] = Reservation.EventTypeChoices.CLUB_RESERVATION
            request.data["reason"] = Reservation.LockReasonChoices.CLUB_RESERVATION


        if settings.DEBUG :
            self.__logger.warning(f"ReservationViewSet.create() - request.data : {request.data} ")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk=None):
         if settings.DEBUG :
             self.__logger.warning(f"Updating reservation: \n<{pk}>  , {request.body} ")

         reservation = Reservation.objects.filter(pk=pk)

         serializer = self.serializer_class(instance=reservation,data=request.data, partial=True)
         serializer.is_valid(raise_exception=True)

         if (settings.DEBUG):
             self.__logger.warning(f"Updating reservation validated_data: {serializer.validated_data} ")

         updatedMember = serializer.save()

         return Response(updatedMember)

    def destroy(self, request, pk=None):
        """
        Delete a reservation
        """
        if settings.DEBUG :
            self.__logger.warning({"message" : f"ReservationViewSet.destroy() - request.body : {request.body}"})

        try:
            reservation = Reservation.objects.get(pk=pk)

            if not reservation :
                raise APIException({ "message" : "Reservation does not exist" })

            if not request.user.is_staff and reservation.author.id != request.user.id :
                raise APIException({ "message" : "Member can only delete their reservations!"})

            diff = datetime.combine(reservation.date_reservation, reservation.start_time) - datetime.now()

            if diff < timedelta(hours=24):
                raise APIException(
                    {'message': 'Reservation cannot be deleted 24 hours before reservation''s start time.'})

            # Delete reservation
            reservation.delete()
        except Reservation.DoesNotExist:
            raise APIException({'message': 'Reservation does not exist.'})


        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def me(self, request):
        """
        Get authenticated user's reservations
        """
        # We exclude all event created by Admin member
        serializer = self.serializer_class(
            self.queryset.filter(author=request.user).exclude(event_type=Reservation.EventTypeChoices.EVENT),
            many=True
        )

        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def by_court(self, request):
        """
        Get reservations grouped by court
        """

        serializer = CourtReservationSerializer(
            Court.objects.all().prefetch_related("reservations"),
            many=True
        )


        return Response(serializer.data)