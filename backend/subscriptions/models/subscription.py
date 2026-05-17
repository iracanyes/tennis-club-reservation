import uuid
from django.db import models

from members.models import Member


class Subscription(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'subscription'
    ordering = ['-date_created']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(name='date_created', auto_now_add=True)
  year = models.IntegerField()
  fee = models.DecimalField(max_digits=10, decimal_places=2)
  paid_in_cash = models.BooleanField(name='paid_in_cash', default=False)
  reference = models.CharField(max_length=255)

  member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='subscriptions')


  def __str__(self):
    return f"""
    {{
      'id' : {self.id},
      'dateCreated' : {self.date_created},
      'year' : {self.year},
      'fee' : {self.fee},
      'paidInCash' : {self.paid_in_cash},
      'reference' : {self.reference},
      'member' : {self.member},
    }}
    """