import uuid
from datetime import datetime

from django.utils import timezone

from members.models import Member
from reservations.models import Court
from django.db import models
from django.utils.translation import gettext_lazy as _

class Reservation(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'reservation'
    ordering = ['-date_reservation']
    # TODO: Make constraint for start_time for closing in range
    # constraints = [
    #   models.CheckConstraint(
    #     name="check_start_time",
    #   )
    # ]

  class EventTypeChoices(models.TextChoices):
    CLUB_RESERVATION = 'club_reservation', _("Club Reservation")
    EVENT = 'event', _("Event")
    UNKNOWN = 'unknown', _("Unknown")

  class DurationChoices(models.IntegerChoices):
    ONE_HOUR = 1, _("One hour")
    TWO_HOURS = 2, _("Two hours")
    FOUR_HOURS = 4, _("Four hours")
    ONE_DAY = 13, _("One day")

  class StatusChoices(models.TextChoices):
    ACTIVE = 'active', _("Active")
    COMPLETED = 'completed', _("Completed")
    CANCELED = 'canceled', _("Canceled")
    UNCOMPLETED = 'uncompleted', _("Uncompleted")

  class LockReasonChoices(models.TextChoices):
    CLUB_RESERVATION = 'club_reservation', _('Club Reservation')
    INTERCLUBS = 'interclubs', _('Interclubs')
    CHAMPIONSHIP = 'championship', _('Championnat')
    COMPETITION = 'competition', _('Compétition')
    LESSON = 'lesson', _('Cours')
    RENOVATION = 'renovation', _('Rénovation')


  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(name='date_created', auto_now_add=True)
  date_modified = models.DateTimeField(name='date_modified', auto_now=True)
  date_reservation = models.DateField(name='date_reservation')
  start_time = models.TimeField(name='start_time')
  duration = models.IntegerField(choices=DurationChoices, default=DurationChoices.ONE_HOUR)
  status = models.CharField(max_length=255, choices=StatusChoices, default=StatusChoices.ACTIVE)
  is_double = models.BooleanField(name='is_double', default=False)
  event_type = models.CharField(max_length=50, choices=EventTypeChoices, default=EventTypeChoices.UNKNOWN)
  reason = models.CharField(max_length=255, choices=LockReasonChoices, default=LockReasonChoices.CLUB_RESERVATION)

  author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')
  court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='reservations')
  participants = models.ManyToManyField(Member, related_name='participations')

  def __str__(self):
    return f"""Reservation{{ 
      'id' : {self.id}, 
      'date_created' : {self.date_created}, 
      'date_modified' : {self.date_modified},
      'event_type' : {self.event_type}, 
      'reason' : {self.reason},
      'reason' : {self.reason},      
      'date_reservation' : {self.date_reservation},
      'duration' : {self.duration}, 
      'start_time' : {self.start_time},
      'status' : {self.status},
      'isDouble' : {self.is_double},
      'author' : {self.author},
      'court' : {self.court},
      'participants' : {self.participants},
    }}
    """