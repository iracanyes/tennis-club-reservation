from rest_framework import serializers
from django.contrib.auth import authenticate


class AdminLoginGoogleSerializer(serializers.Serializer):
    credentials = serializers.CharField()

    def validate(self, data):
        try:
            admin = authenticate(token=data["credentials"])

            if not admin:
                raise serializers.ValidationError("Admin not found.")

            data['admin'] = admin

            return data
        except ValueError:
            raise serializers.ValidationError("Invalid credentials.")