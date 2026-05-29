from django.db import models
import uuid

from . import Court


class TimeSlot(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'time_slot'
    ordering = ['-date', 'start_time', 'end_time']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField(name='date_created', auto_now_add=True)
  date = models.DateField()
  start_time = models.TimeField(name='start_time')
  end_time = models.TimeField(name='end_time')
  status = models.CharField(max_length=100)

  court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='time_slots')


  def __str__(self):
    return f"""TimeSlot{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'date' : {self.date}, 
      'startTime' : {self.start_time},
      'endTime' : {self.end_time},
      'status' : {self.status},
      'court': {self.court},     
    }}
    """