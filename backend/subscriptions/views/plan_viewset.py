from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Plan
from subscriptions.serializers import PlanSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List all plans
        """
        serializer = PlanSerializer(self.queryset, many=True)

        return Response(serializer.data)
