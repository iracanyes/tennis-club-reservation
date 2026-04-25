from django.db import models
import uuid

from . import Court, CourtEvent


class TimeSlot(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'time_slot'
    ordering = ['-date', 'start_time', 'end_time']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField(name='date_created')
  date = models.DateField()
  startTime = models.TimeField(name='start_time')
  endTime = models.TimeField(name='end_time')
  status = models.CharField(max_length=100)

  court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='time_slots')


  def __str__(self):
    return f"""TimeSlot{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'date' : {self.date}, 
      'startTime' : {self.startTime},
      'endTime' : {self.endTime},
      'status' : {self.status},
      'court': {self.court},     
    }}
    """