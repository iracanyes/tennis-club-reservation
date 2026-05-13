from django.contrib.auth import authenticate
from rest_framework import serializers

from members.models import Member
from members.models.member import member_aft_number_validator


class ChangePasswordSerializer(serializers.Serializer):
    aft_id = serializers.CharField(max_length=7, validators=[member_aft_number_validator])
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        print(f"ChangePasswordSerializer validate - data : {data}")

        member = authenticate(aft_id=data['aft_id'], password=data['password'])

        if not member:
            raise serializers.ValidationError("Aucun membre ne correspond aux identifiants fournis.")



        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("Les nouveaux mots de passe fournit ne correspondent pas.")

        data["member"] = member

        return data