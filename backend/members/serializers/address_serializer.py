from rest_framework import serializers

from members.models import Address


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ['id', 'street', 'number', 'city', 'state', 'zip_code', 'country']