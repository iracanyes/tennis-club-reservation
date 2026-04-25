from rest_framework import viewsets, permissions
from members.serializers import MemberSerializer, CategorySerializer
from members.models import Member, Address, Category, MemberRank, Rank


class MemberViewSet(viewsets.ModelViewSet):
  queryset = Member.objects.all().order_by('-date_joined')
  serializer_class = MemberSerializer
  permission_classes = [permissions.IsAuthenticated]



class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Member.objects.all().order_by('-date_joined')
  serializer_class = CategorySerializer
  permission_classes = [permissions.IsAuthenticated]
