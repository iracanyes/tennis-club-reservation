from django.contrib.auth import authenticate
from rest_framework import serializers
from administrators.models import Admin
from members.serializers.address_serializer import AddressSerializer


class AdminSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ["id", 'email', 'aftId', 'firstname', 'lastname', 'birthdate', 'gender', 'phoneNumber', 'annualFeePaid', 'is_staff', 'is_active', 'address']


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        admin = authenticate(email=data['email'], password=data['password'])

        if not admin:
            raise serializers.ValidationError("Email or password is incorrect.")

        data["admin"] = admin

        return data
