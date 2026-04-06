import uuid
from django.db import models

class CourtEvent(models.Model):
  class Meta:
    # abstract class not include in the model (no table created by Django ORM
    # Remark : Abstract class can't have relationships
    #abstract = True
    db_table = 'court_event'
    ordering = ['-dateReservation']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField(auto_now_add=True)
  dateModified = models.DateTimeField(auto_now=True)
  dateReservation = models.DateField()
  event_type = 'generic'
  status = models.CharField(max_length=255)

  def __str__(self):
    return f"""CourtEvent{{ 
      'id' : {self.id}, 
      'dateCreate' : {self.dateCreated}, 
      'dateModified' : {self.dateModified}, 
      'event_type' : {self.event_type}, 
      'status' : {self.status},
    }}
    """
