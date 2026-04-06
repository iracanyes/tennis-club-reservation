import uuid
from django.db import models

from . import Member


class Subscription(models.Model):
  class Meta:
    db_table = 'subscription'
    ordering = ['-dateCreated']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField()
  year = models.IntegerField()
  fee = models.FloatField()
  paidInCash = models.BooleanField()
  reference = models.CharField(max_length=50)

  member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='subscriptions')


  def __str__(self):
    return f"""
    {{
      'id' : {self.id},
      'dateCreated' : {self.dateCreated},
      'year' : {self.year},
      'fee' : {self.fee},
      'paidInCash' : {self.paidInCash},
      'reference' : {self.reference},
      'member' : {self.member},
    }}
    """