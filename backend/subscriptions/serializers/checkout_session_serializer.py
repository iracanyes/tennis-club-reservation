from rest_framework import serializers
from subscriptions.models import Plan

class CheckoutSessionSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)

    def validate(self, data):
        print(f"CheckoutSessionSerializer.validate() - data: {type(data)} => {data}")

        plan = Plan.objects.get(pk=data['id'])

        if plan is None:
            raise serializers.ValidationError("Plan doesn't exist")

        data['plan'] = plan

        return data