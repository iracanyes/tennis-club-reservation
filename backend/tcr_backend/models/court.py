import uuid
from django.db import models

class Court(models.Model):
  class Meta:
    db_table = 'court'
    ordering = ['number']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  number = models.IntegerField(default=1)
  type = models.CharField(max_length=20)

  def __str__(self):
    return f"""Court{{
      'number' : {self.number}, 
      'type' : {self.type}
    }}
    """