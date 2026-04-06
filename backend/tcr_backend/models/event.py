from . import CourtEvent, Administrator
from django.db import models


class Event(CourtEvent):
  class Meta:
    db_table = 'event'
    ordering = ['-dateReservation']

  description = models.CharField(max_length=255)
  isAllDay = models.BooleanField(default=False)
  event_type = 'external_event'

  author = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='events')

  def __str__(self):
    return f"""Event{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'dateModified' : {self.dateModified}, 
      'event_type' : {self.event_type}, 
      'status' : {self.status},
      'description' : {self.description},
      'isAllDay' : {self.isAllDay},
      'author' : {self.author},      
    }}
    """
