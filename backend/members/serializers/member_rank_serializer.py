from rest_framework import serializers

from members.models import Member, MemberRank, Rank
from . import RankSerializer


class MemberRankSerializer(serializers.ModelSerializer):
  rank_id = serializers.PrimaryKeyRelatedField(queryset=Rank.objects.all(), write_only=True, source='rank')
  rank = RankSerializer(read_only=True)
  points = serializers.FloatField()



  class Meta:
    model = MemberRank
    fields = ['id', 'date_created', 'points', 'member_id', 'rank_id', 'rank']
    # Par défaut, DRF génère automatiquement des validateurs d'unicité basés sur les contraintes de la base de données.
    # Pour éviter que le MemberRankSerializer ne bloque la requête avant même d'arriver à la méthode update du membre,
    # il faut vider explicitement la liste de ses validateurs par défaut
    validators = []