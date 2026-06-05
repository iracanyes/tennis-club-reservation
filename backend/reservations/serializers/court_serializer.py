import logging

from rest_framework import serializers, exceptions
from reservations.models import Court


class CourtSerializer(serializers.ModelSerializer):
    __logger = logging.getLogger(__name__)



    class Meta:
        model = Court
        fields = '__all__'


    def create(self, validated_data):
        try:
            court = Court.objects.create(**validated_data)

        except exceptions.ValidationError as e:
            self.__logger.error(f"Court creation failed : {e}")
            raise exceptions.ValidationError(f"Court creation failed")

        return court

    def update(self, instance, validated_data):
        try:

            instance.number = validated_data['number']
            instance.type = validated_data['type']

            instance.save()
        except Court.DoesNotExist:

            raise exceptions.ValidationError("Court does not exist")

        return instance


