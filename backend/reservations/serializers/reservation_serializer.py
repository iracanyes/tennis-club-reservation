import logging
from datetime import timedelta, datetime, date, time
from dateutil.relativedelta import relativedelta, SU, SA
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import APIException

from members.serializers import MemberReservationSerializer
from members.models import Member
from reservations.models import Court, Reservation, TimeSlot
from reservations.serializers import CourtSerializer


class ReservationSerializer(serializers.ModelSerializer):
    __logger = logging.getLogger(__name__)

    author = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    court = serializers.PrimaryKeyRelatedField(queryset=Court.objects.all())
    participants = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), many=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "date_created",
            "date_modified",
            "date_reservation",
            "start_time",
            "duration",
            "is_double",
            "status",
            "event_type",
            "court",
            "author",
            "participants"
        ]


    def validate(self, data):
        if settings.DEBUG :
            self.__logger.warning(f"ReservationSerializer.validate - data: {data}")

        #author = Member.objects.get(id=data['author']['id'])

        if not data['author'] :
            raise serializers.ValidationError({'message': 'Author not found.'})

        #court = Court.objects.get(id=data['court']['id'])

        if not data['court'] :
            raise serializers.ValidationError({'message': 'Court not found.'})

        # participants = []
        # for participant in data['participants']:
        #     participants.append(Member.objects.get(id=participant['id']))
        #
        # data['participants'] = participants
        # data['author'] = author
        # data['court'] = court

        return data

    def create(self, validated_data):

        if(settings.DEBUG):
            self.__logger.warning(f"ReservationSerializer.create - validated_data: {validated_data}")

        # Check opening hour
        if validated_data["start_time"] < time(9,0):
            raise serializers.ValidationError({ "message" : "The club reservation only open at 09:00 AM."})


        # Check closing hour
        if validated_data['start_time'] > time(18, 0) :
            if validated_data["duration"] == Reservation.DurationChoices.FOUR_HOURS:
                raise serializers.ValidationError({'message': 'Reservation end time exceed closing hour 22h.'})

            if validated_data['start_time'] > time(20, 0):
                if validated_data['duration'] > Reservation.DurationChoices.TWO_HOURS:
                    raise serializers.ValidationError({'message': 'Reservation end time exceed closing hour 22h.'})

                if validated_data['start_time'] > time(21, 0):
                    if validated_data["duration"] > Reservation.DurationChoices.ONE_HOUR:
                        raise serializers.ValidationError({'message': 'Reservation end time exceed closing hour 22h.'})



        #
        if(validated_data['is_double']):

            # Check if no reservation for this date and timeslot exists,
            reservationExists = Reservation.objects.filter(
                date_reservation=validated_data['date_reservation'],
                start_time__range=(validated_data['start_time'], (datetime.combine(date.today(), validated_data['start_time']) + timedelta(hours=1)).time()),
                court__id=validated_data["court"].id
            ).exists()
        else:

            # Check if no reservation for this date and timeslot exists,
            reservationExists = Reservation.objects.filter(
                date_reservation=validated_data['date_reservation'],
                start_time=validated_data['start_time']
            ).exists()

        if reservationExists:
            raise serializers.ValidationError({'message': 'Reservation already exists for this date and time on this court.'})

        # TODO: Checks for max week reservation by member. Week start on sunday -> saturday
        # 1. Max 2 hours of simple reservation by week
        # 2. Max 4 hours of double reservation by week

        last_sunday = validated_data['date_reservation'] + relativedelta(weekday=SU(-1))
        next_saturday = validated_data['date_reservation'] + relativedelta(weekday=SA(1))

        if settings.DEBUG :
            self.__logger.debug(f"ReservationSerializer.create - validated_dataauthor__id=validated_data['author'] : {validated_data['author']}")

        # Check last member's reservation for this week
        memberReservations = Reservation.objects.filter(
            author__id=validated_data['author'].id,
            date_reservation__range=(last_sunday, next_saturday),
        )

        if memberReservations.count() == 2 :
            raise APIException({'message': 'Member has reached the max number of reservations for this week.'})

        memberReservation = memberReservations.first()



        # 3. One hour of simple ou two hours of double
        if validated_data['is_double']:
            if memberReservation is not None :
                if not memberReservation.is_double :
                    raise APIException({'message': 'Member has already a simple reservation booked for this week.'})
                # Check if the first reservation reach max hours for double reservation
                if memberReservation.duration == Reservation.DurationChoices.FOUR_HOURS :
                    raise APIException({"message" : "Member has reached the max number of double reservation for this week."})
        else:
            if memberReservation is not None:
                if memberReservation.is_double :
                    raise APIException({ 'message' : 'Member has already a double reservation booked for this week.'})
                # Check if first reservation doesn't reach max hours for simple reservation
                if memberReservation.duration == Reservation.DurationChoices.TWO_HOURS :
                    raise APIException({ "message" : "Member has reached the max number of simple reservation for this week." })

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
            status=Reservation.StatusChoices.ACTIVE,
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



