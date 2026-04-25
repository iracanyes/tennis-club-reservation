import uuid
from django.db import models

from members.models import Member


class Subscription(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'subscription'
    ordering = ['-date_created']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField(name='date_created')
  year = models.IntegerField()
  fee = models.FloatField()
  paidInCash = models.BooleanField(name='paid_in_cash', default=False)
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