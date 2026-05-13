from rest_framework import serializers

from members.models import Address


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ['id', 'street', 'number', 'city', 'state', 'zip_code', 'country']

  def update(self, instance, validated_data):

    instance.street = validated_data.get('street', instance.street)
    instance.number = validated_data.get('number', instance.number)
    instance.city = validated_data.get('city', instance.city)
    instance.state = validated_data.get('state', instance.state)
    instance.zip_code = validated_data.get('zip_code', instance.zip_code)
    instance.country = validated_data.get('country', instance.country)

    instance.save()

    return instance