import uuid
from django.db import models

from . import Member, Rank


class MemberRank(models.Model):
  class Meta:
    db_table = 'member_rank'
    ordering = ['-dateCreated']

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  dateCreated = models.DateTimeField(auto_now_add=True)
  points = models.FloatField()

  # Relationships
  member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='memberRanks')
  rank = models.ForeignKey(Rank, on_delete=models.CASCADE, related_name='members')

  def __str__(self):
    return f"""
    {{
      'id' : {self.id},
      'dateCreated' : {self.dateCreated},
      'points' : {self.points},
      'member' : {self.member},
      'rank' : {self.rank},
    }}
    """
