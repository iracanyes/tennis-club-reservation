from django.db import models
import uuid

from . import Court, CourtEvent


class TimeSlot(models.Model):
  class Meta:
    db_table = 'time_slot'
    ordering = ['-date', 'startTime', 'endTime']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField()
  date = models.DateField()
  startTime = models.TimeField()
  endTime = models.TimeField()
  status = models.TextField()

  courtEvent = models.ForeignKey(CourtEvent, on_delete=models.CASCADE, related_name='timeSlots')
  court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='timeSlots')

  def __str__(self):
    return f"""TimeSlot{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'date' : {self.date}, 
      'startTime' : {self.startTime},
      'endTime' : {self.endTime},
      'status' : {self.status},
      'courtEvent' : {self.courtEvent},
      'court' : {self.court},         
    }}
    """