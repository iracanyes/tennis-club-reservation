import uuid
from django.db import models
from members.models import Member
from . import Court

class CourtEvent(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    # abstract class not include in the model (no table created by Django ORM
    # Remark : Abstract class can't have relationships
    #abstract = True
    db_table = 'court_event'
    ordering = ['-date_reservation']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField(name='date_created', auto_now_add=True)
  dateModified = models.DateTimeField(name='date_modified', auto_now=True)
  dateReservation = models.DateField(name='date_reservation')
  eventType = 'generic'
  status = models.CharField(max_length=255)

  court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='court_events')
  participants = models.ManyToManyField(Member, related_name='participations')

  def __str__(self):
    return f"""CourtEvent{{ 
      'id' : {self.id}, 
      'dateCreated' : {self.dateCreated}, 
      'dateModified' : {self.dateModified}, 
      'eventType' : {self.eventType}, 
      'status' : {self.status},
      'court' : {self.court},
      'participants' : {self.participants},
    }}
    """
