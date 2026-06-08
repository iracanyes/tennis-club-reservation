from rest_framework import serializers
from members.models import Category


class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    fields = ['id', 'name', 'description', 'age_min', 'age_max', 'birth_year_min', 'birth_year_max', 'gender']
