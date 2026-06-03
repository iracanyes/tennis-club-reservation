import logging
from datetime import timedelta, datetime, date

from django.conf import settings
from rest_framework import serializers
from reservations.models import Reservation, TimeSlot
from reservations.validators import ReservationValidator
from . import ReservationSerializer


class EventSerializer(ReservationSerializer):
    __logger = logging.getLogger(__name__)

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        super().validate(data)

        if data['event_type'] == Reservation.EventTypeChoices.CLUB_RESERVATION:
            raise serializers.ValidationError("Event type must other than CLUB_RESERVATION")

        if data["reason"] == Reservation.LockReasonChoices.CLUB_RESERVATION:
            raise serializers.ValidationError("Event's reason must not be CLUB_RESERVATION")

        if not data["author"].is_staff:
            raise serializers.ValidationError("Author must be a staff member")

        return data

    def create(self, validated_data):
        if settings.DEBUG:
            self.__logger.warning(f"ReservationSerializer.create - validated_data: {validated_data}")

            # Check opening hour
        ReservationValidator.check_opening_hour(validated_data)

        # Check closing hour
        ReservationValidator.check_closing_hour(validated_data)

        # Check if no reservation for this date and timeslot exists,
        ReservationValidator.check_reservation_already_exists(validated_data)


        # Inputs
        duration = None
        event_type = Reservation.EventTypeChoices.EVENT
        reason = None

        # duration's choices
        durationChoices = [durationChoice.value for durationChoice in Reservation.DurationChoices]

        if validated_data["duration"] in durationChoices:
            duration = validated_data["duration"]
        else:
            serializers.ValidationError("Event duration must be one of {}".format(durationChoices))

        reasons = [reasonChoice.value for reasonChoice in Reservation.LockReasonChoices]
        if validated_data["reason"] in reasons:
            reason = validated_data["reason"]
        else:
            serializers.ValidationError("Reason must be one of {}".format(reasons))

        reservation = Reservation(
            date_reservation=validated_data["date_reservation"],
            start_time = validated_data["start_time"],
            duration=duration,
            is_double=validated_data["is_double"],
            event_type=event_type,
            reason=reason,
            status=Reservation.StatusChoices.ACTIVE,

        )

        # Set relations
        reservation.court = validated_data["court"]
        reservation.author = validated_data["author"]

        # Create court's timeslot for the event
        endTime = None

        if validated_data["duration"] in durationChoices:
            endTime = (datetime.combine(date.today(), validated_data['start_time']) + timedelta(hours=validated_data["duration"])).time()

        timeslot = TimeSlot(
            date=validated_data["date_reservation"],
            start_time=validated_data["start_time"],
            end_time=endTime,
            status=TimeSlot.StatusChoices.RESERVED,
            court=validated_data["court"],
        )

        # Save reservation
        reservation.save()

        # Save reservation's participants
        for participant in validated_data['participants']:
            reservation.participants.add(participant)

        reservation.save()

        # Save Court's timeslot
        timeslot.save()

        return reservation

    def update(self, instance, validated_data):
        pass

    def partial_update(self, instance, validated_data):
        pass

