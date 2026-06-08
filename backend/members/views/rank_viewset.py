from rest_framework import viewsets, permissions
from rest_framework.response import Response

from members.serializers import RankSerializer
from members.models import Rank


class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        List all ranks
        """
        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)