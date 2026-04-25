from rest_framework import serializers

from members.models import MemberRank
from serializers.rank_serializer import RankSerializer


class MemberRankSerializer(serializers.ModelSerializer):
  rank = RankSerializer(read_only=True)

  class Meta:
    model = MemberRank
    fields = ['id', 'member_id', 'date_created', 'points', 'rank']