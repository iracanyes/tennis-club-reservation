from . import CourtEvent
from administrators.models import Admin
from django.db import models


class Event(CourtEvent):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'event'
    ordering = ['-date_reservation']

  description = models.TextField()
  isAllDay = models.BooleanField(default=False)
  eventType = 'external_event'

  author = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='events')

  def __str__(self):
    return f"""Event{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'dateModified' : {self.dateModified}, 
      'event_type' : {self.eventType}, 
      'status' : {self.status},
      'description' : {self.description},
      'isAllDay' : {self.isAllDay},
      'author' : {self.author},
      'court' : {self.court},      
    }}
    """
