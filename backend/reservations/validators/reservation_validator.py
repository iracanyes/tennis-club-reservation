import logging
from dateutil.relativedelta import relativedelta, SU, SA
from django.conf import settings
from datetime import time, datetime, date, timedelta

from django.db.models import Model
from rest_framework import serializers
from reservations.models import Reservation, TimeSlot





class ReservationValidator:
    __logger = logging.getLogger(__name__)

    @staticmethod
    def check_opening_hour(data):
        if data["start_time"] < time(9, 0):
            raise serializers.ValidationError({"message": "The club reservation only open at 09:00 AM."})

    @staticmethod
    def check_closing_hour(data):


        if data['start_time'] > time(18, 0) :
            if data["duration"] == Reservation.DurationChoices.FOUR_HOURS:
                raise serializers.ValidationError({'message': 'Reservation end time exceed closing hour 22h.'})

            if data['start_time'] > time(20, 0):
                if data['duration'] > Reservation.DurationChoices.TWO_HOURS:
                    raise serializers.ValidationError({'message': 'Reservation end time exceed closing hour 22h.'})

                if data['start_time'] > time(21, 0):
                    if data["duration"] > Reservation.DurationChoices.ONE_HOUR:
                        raise serializers.ValidationError({'message': 'Reservation end time exceed closing hour 22h.'})

        if data["duration"] == Reservation.DurationChoices.ONE_DAY and  data["event_type"] == Reservation.EventTypeChoices.EVENT and data["start_time"] > time(9, 0) :
            raise serializers.ValidationError( {"message": "Reservation for one day must start at 09:00 AM."})

    @staticmethod
    def check_reservation_already_exists(data):
        reservation_exists = False

        try:
            if (data['duration'] > 1):



                # Check if no reservation for this court and date starts in the start time and duration range of the new reservation,
                reservation_exists = Reservation.objects.filter(
                    date_reservation=data['date_reservation'],
                    start_time__range=(
                        data['start_time'],
                        (
                                datetime.combine(date.today(), data['start_time']) + timedelta(hours=data['duration'])
                        ).time()
                    ),
                    court__id=data["court"].id
                ).exists()

                if not reservation_exists :
                    # Check if no reservation for this court ends in the start_time, duration range of the new reservation
                    # Here we use TimeSlot which compute the end time of each reservation
                    reservation_exists = TimeSlot.objects.filter(
                        date=data['date_reservation'],
                        court__id=data["court"].id,
                        end_time__range=(
                            data['start_time'],
                            (
                                    datetime.combine(date.today(), data['start_time']) + timedelta(
                                hours=data['duration'])
                            ).time()
                        )
                    ).exists()


                if not reservation_exists and data["duration"] == Reservation.DurationChoices.TWO_HOURS:
                    reservation_exists = Reservation.objects.filter(
                        date_reservation=data['date_reservation'],
                        court__id=data["court"].id,
                        duration=Reservation.DurationChoices.FOUR_HOURS,
                        start_time=(datetime.combine(date.today(), data['start_time']) - timedelta(hours=1)).time()
                    ).exists()


                if not reservation_exists:
                    # Check if no all day event exists on this court for this date
                    reservation_exists = Reservation.objects.filter(
                        date_reservation=data['date_reservation'],
                        court__id= data["court"].id,
                        event_type=Reservation.EventTypeChoices.EVENT,
                        duration=Reservation.DurationChoices.ONE_DAY,
                    ).exists()



            else:
                # Check if no reservation for this date and timeslot exists,
                reservation_exists = Reservation.objects.filter(
                    date_reservation=data['date_reservation'],
                    start_time=data['start_time']
                ).exists()

        except Exception as e:
            ReservationValidator.__logger.error(f"{e}")
            raise serializers.ValidationError( {"message": "An error occured while checking if reservation already exists."})

        if settings.DEBUG:
            ReservationValidator.__logger.warning(f"Reservation start in range exists : {reservation_exists}")

        if reservation_exists :
            raise serializers.ValidationError(
                {'message': "Une réservation existe déjà pour ce terrain à l'heure sélectionnée."})



    @staticmethod
    def check_reservation_limit_by_week(data):
        last_sunday = data['date_reservation'] + relativedelta(weekday=SU(-1))
        next_saturday = data['date_reservation'] + relativedelta(weekday=SA(1))

        if settings.DEBUG:
            ReservationValidator.__logger.debug(f"ReservationSerializer.create - data['author'] : {data['author']}")

        # Check last member's reservation for this week
        memberReservations = Reservation.objects.filter(
            author__id=data['author'].id,
            date_reservation__range=(last_sunday, next_saturday),
        )

        if memberReservations.count() == 2:
            raise serializers.ValidationError({'message': 'Member has reached the max number of reservations for this week.'})

        memberReservation = memberReservations.first()

        # 3. One hour of simple or two hours of double
        if data['is_double']:
            if memberReservation is not None:
                if not memberReservation.is_double:
                    raise serializers.ValidationError({'message': 'Member has already a simple reservation booked for this week.'})
                # Check if the first reservation reach max hours for double reservation
                if memberReservation.duration == Reservation.DurationChoices.FOUR_HOURS:
                    raise serializers.ValidationError(
                        {"message": "Member has reached the max number of double reservation for this week."})
        else:
            if memberReservation is not None:
                if memberReservation.is_double:
                    raise serializers.ValidationError({'message': 'Member has already a double reservation booked for this week.'})
                # Check if first reservation doesn't reach max hours for simple reservation
                if memberReservation.duration == Reservation.DurationChoices.TWO_HOURS:
                    raise serializers.ValidationError(
                        {"message": "Member has reached the max number of simple reservation for this week."})

    @staticmethod
    def check_max_hours_per_reservation(data):
        if data["event_type"] == Reservation.EventTypeChoices.CLUB_RESERVATION and (data["duration"] > Reservation.DurationChoices.FOUR_HOURS):
            raise serializers.ValidationError( {"message": "Club reservation has a limit of max 4 hours per reservation."})


    @staticmethod
    def check_annual_fee_paid(data):
        if not data["author"].annual_fee_paid:
            raise serializers.ValidationError( {"message": "Reservations not allowed as member hasn't pay his annual fee."})