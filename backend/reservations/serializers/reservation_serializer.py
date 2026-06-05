import logging
from datetime import timedelta, datetime, date, time
from dateutil.relativedelta import relativedelta, SU, SA
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import APIException

from members.serializers import MemberReservationSerializer
from members.models import Member
from reservations.models import Court, Reservation, TimeSlot
from reservations.serializers import CourtSerializer
from reservations.validators import ReservationValidator


class ReservationSerializer(serializers.ModelSerializer):
    __logger = logging.getLogger(__name__)

    # Used to write (create or update) a reservation and attach the author's reference without attempt to create a new member
    author_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), write_only=True, source="author")
    # Only accessible on read
    author = MemberReservationSerializer(read_only=True)

    court_id = serializers.PrimaryKeyRelatedField(queryset=Court.objects.all(), write_only=True, source="court")
    court = CourtSerializer(read_only=True)

    participants_ids = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        write_only=True,
        source="participants",
        many=True,

    )
    participants = MemberReservationSerializer(read_only=True, many=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "date_created",
            "date_modified",
            "event_type",
            "reason",
            "date_reservation",
            "start_time",
            "duration",
            "is_double",
            "status",
            "court_id",
            "court",
            "author_id",
            "author",
            "participants_ids",
            "participants"
        ]


    def validate(self, data):
        if settings.DEBUG :
            self.__logger.warning(f"ReservationSerializer.validate - data: {data}")

        if not 'author_id' in data and not "author" in data :
            raise serializers.ValidationError({'message': 'Author not found.'})

        if not 'court_id' in data and not "court" in data :
            raise serializers.ValidationError({'message': 'Court or court ID not provided.'})

        if not 'participants_ids' in data and not "participants" in data :
            raise serializers.ValidationError({'message': 'participants not found.'})

        status_choices = [status_choice.value for status_choice in Reservation.StatusChoices]

        if not data["status"] in status_choices:
            raise serializers.ValidationError({'message': f'Status must be one of [{", ".join(status_choices)}] .'})

        return data

    def create(self, validated_data):

        if(settings.DEBUG):
            self.__logger.warning(f"ReservationSerializer.create - validated_data: {validated_data}")

        # Check opening hour
        ReservationValidator.check_opening_hour(validated_data)

        # Check closing hour
        ReservationValidator.check_closing_hour(validated_data)

        # Check if no reservation for this date and timeslot exists,
        ReservationValidator.check_reservation_already_exists(validated_data)

        # TODO: Checks for max week reservation by member. Week start on sunday -> saturday
        # 1. Max 2 hours of simple reservation by week
        # 2. Max 4 hours of double reservation by week
        ReservationValidator.check_reservation_limit_by_week(validated_data)



        # event type input
        if validated_data['event_type'] ==  Reservation.EventTypeChoices.EVENT and validated_data["author"].is_staff :
            eventType =  Reservation.EventTypeChoices.EVENT
        else:
            eventType = Reservation.EventTypeChoices.CLUB_RESERVATION

        # Duration input
        duration = None
        match validated_data['duration'] :
            case Reservation.DurationChoices.ONE_HOUR:
                duration = Reservation.DurationChoices.ONE_HOUR
            case Reservation.DurationChoices.TWO_HOURS:
                duration = Reservation.DurationChoices.TWO_HOURS
            case Reservation.DurationChoices.FOUR_HOURS:
                duration = Reservation.DurationChoices.FOUR_HOURS
            case Reservation.DurationChoices.ONE_DAY:
                duration = Reservation.DurationChoices.ONE_DAY


        # TODO : create reservation
        reservation = Reservation(
            date_reservation = validated_data['date_reservation'],
            start_time=validated_data['start_time'],
            duration=duration,
            is_double = validated_data['is_double'],
            status = Reservation.StatusChoices.ACTIVE,
            event_type = eventType,

        )

        # Set relations
        reservation.court = validated_data['court']
        reservation.author = validated_data['author']



        endTime = None
        match validated_data['duration'] :
            case Reservation.DurationChoices.ONE_HOUR:
                endTime = (datetime.combine(date.today(), validated_data['start_time']) + timedelta(hours=1)).time()
            case Reservation.DurationChoices.TWO_HOURS:
                endTime = (datetime.combine(date.today(), validated_data['start_time']) + timedelta(hours=2)).time()
            case Reservation.DurationChoices.FOUR_HOURS:
                endTime = (datetime.combine(date.today(), validated_data['start_time']) + timedelta(hours=4)).time()
            case Reservation.DurationChoices.ONE_DAY:
                endTime = time(22,0)


        # TODO : Mark the timeslot as reserved
        timeslot = TimeSlot(
            date=validated_data['date_reservation'],
            start_time=validated_data['start_time'],
            end_time=endTime,
            status=TimeSlot.StatusChoices.RESERVED,
            court=validated_data['court'],
        )

        # Save instances
        reservation.save()

        # Save reservation's participants
        for participant in validated_data['participants']:
            reservation.participants.add(participant)

        reservation.save()

        # Save Court's timeslot
        timeslot.save()

        return reservation

    def update(self, instance, validated_data):

        instance.status = validated_data['status']
        instance.save()

        return instance


class ReservationDeleteSerializer(ReservationSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "date_reservation", "start_time", "author"]

    def validate(self, data):
        try:
            reservation = Reservation.objects.get(pk=data['id'])

            if not reservation:
                raise APIException({'message': 'Reservation does not exist.'})

            diff = datetime.combine(reservation.date_reservation, reservation.start_time) - datetime.now()

            if diff < timedelta(hours=24):
                raise APIException(
                    {'message': 'Reservation cannot be deleted 24 hours before reservation''s start time.'})

            data["reservation"] = reservation
        except Reservation.DoesNotExist:
            raise serializers.ValidationError({'message': 'Reservation does not exist.'})


        return data


class ReservationWithoutCourtSerializer(ReservationSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        
    court = None
