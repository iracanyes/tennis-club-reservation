
from members.models import Member
from . import CourtEvent
from django.db import models

class Reservation(CourtEvent):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'reservation'
    ordering = ['-date_reservation']

  isDouble = models.BooleanField(name='is_double', default=False)
  eventType = 'club_reservation'

  author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')


  def __str__(self):
    return f"""Reservation{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'dateModified' : {self.dateModified}, 
      'event_type' : {self.eventType},
      'status' : {self.status},
      'isDouble' : {self.isDouble},
      'author' : {self.author},
      'court' : {self.court},
      'participants' : {self.participants},
    }}
    """