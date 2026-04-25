import uuid
from django.db import models

class Court(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'court'
    ordering = ['number']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  number = models.IntegerField(default=0)
  type = models.CharField(max_length=50)

  def __str__(self):
    return f"""Court{{
      'id' : {self.id},
      'number' : {self.number}, 
      'type' : {self.type}
    }}
    """