import uuid
from django.db import models

class Rank(models.Model):
  class Meta:
    db_table = 'rank'
    ordering = ['name']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  order = models.IntegerField(default=0)
  name = models.CharField(max_length=50)

  def __str__(self):
    return f"""
    {{
      'id': {self.id},
      'name':{self.name},
    }}
    """