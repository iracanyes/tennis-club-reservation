import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Court(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'court'
    ordering = ['number']

  class CourtType(models.TextChoices):
    HARD = 'hard', _('dure')
    CLAY = 'clay', _('battue')
    GRASS = 'grass', _('gazon')
    CARPET = 'carpet', _('moquette')


  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  number = models.IntegerField(default=0, unique=True)
  type = models.CharField(max_length=50, choices=CourtType, default=CourtType.HARD)

  def __str__(self):
    return f"""Court{{
      'id' : {self.id},
      'number' : {self.number}, 
      'type' : {self.type}
    }}
    """