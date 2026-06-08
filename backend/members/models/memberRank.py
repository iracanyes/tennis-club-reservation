import uuid
from django.db import models

from . import Member, Rank


class MemberRank(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'member_rank'
    ordering = ['date_created']
    constraints = [
      # ManyToMany : unique constraint on foreign key
      models.UniqueConstraint(
        fields=["member","rank"],
        name="unique_member_rank",
      )
    ]


  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(name='date_created', auto_now_add=True)
  points = models.FloatField()

  # Relationships
  member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_ranks_entries')
  rank = models.ForeignKey(Rank, on_delete=models.CASCADE)

  def __str__(self):
    return f"""
    {{
      'id' : {self.id},
      'date_created' : {self.date_created},
      'points' : {self.points},
      'member' : {self.member},
      'rank' : {self.rank},
    }}
    """
