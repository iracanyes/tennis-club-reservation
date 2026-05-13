from rest_framework import serializers
from members.models import Category
from members.serializers import MemberSerializer


class CategorySerializer(serializers.ModelSerializer):
  members = MemberSerializer(many=True, read_only=True)

  class Meta:
    model = Category
    fields = ['id', 'name', 'members']
