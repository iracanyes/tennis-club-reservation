from rest_framework import serializers

from reservations.models import Court
from reservations.serializers import ReservationWithoutCourtSerializer


class CourtReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = ["id","number","type", "reservations"]

    reservations = ReservationWithoutCourtSerializer(many=True, read_only=True)