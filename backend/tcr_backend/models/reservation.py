
from . import Member, CourtEvent
from django.db import models

class Reservation(CourtEvent):
  class Meta:
    db_table = 'reservation'
    ordering = ['-dateReservation']

  isDouble = models.BooleanField(default=False)
  event_type = 'reservation'

  author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='ownedReservations')
  participants = models.ManyToManyField(Member, related_name='participants')

  def __str__(self):
    return f"""Reservation{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'dateModified' : {self.dateModified}, 
      'event_type' : {self.event_type},
      'status' : {self.status},
      'isDouble' : {self.isDouble},
      'author' : {self.author},
      'participants' : {self.participants},
    }}
    """