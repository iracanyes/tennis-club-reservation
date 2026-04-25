from rest_framework import serializers

from members.models import Rank


class RankSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rank
    fields = ['id', 'name']