from django.contrib.auth import authenticate
from rest_framework import serializers
from members.models import Member
from .address_serializer import AddressSerializer
from .category_serializer import CategorySerializer


class MemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = ['aft_id', 'firstname', 'lastname', 'email', 'gender', 'birthdate', 'phone_number', 'annual_fee_paid', 'is_superuser', 'is_staff', 'is_active', 'address', 'categories']

class MemberLoginSerializer(serializers.Serializer):
    aft_id = serializers.RegexField(regex=r'^[1-9]\d{6}$')
    password = serializers.CharField(write_only=True)



    def validate(self, data):
        member = authenticate(aft_id=data['aft_id'], password=data['password'])

        #print(f"MemberLoginSerializer.validate: {member}")

        if not member:
            raise serializers.ValidationError("AFT ID or password is incorrect.")

        data["member"] = member

        return data