import uuid
from datetime import datetime
from uuid import UUID
from django.conf import settings
from django.contrib.auth import authenticate
from pip._internal.utils import logging
from rest_framework import serializers
from members.models import Member, Address, Category, MemberRank
from .address_serializer import AddressSerializer
from .category_serializer import CategorySerializer
from .member_rank_serializer import MemberRankSerializer


class MemberSerializer(serializers.ModelSerializer):
    __logger = logging.getLogger(__name__)
    address = AddressSerializer()
    categories_ids = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, source='categories', write_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    member_ranks = MemberRankSerializer(many=True, source="member_ranks_entries")

    class Meta:
        model = Member
        fields = [
            'id',
            'aft_id',
            'email',
            'password',
            'firstname',
            'lastname',
            'gender',
            'birthdate',
            'phone_number',
            'annual_fee_paid',
            'is_superuser',
            'is_staff',
            'is_active',
            'address',
            'categories_ids',
            'categories',
            'member_ranks'
        ]
        extra_kwargs = { 'password' : {'write_only' : True } }



    def create(self, validated_data):
        address = Address(
            street=validated_data['address']['street'],
            number=validated_data['address']['number'],
            city=validated_data['address']['city'],
            state=validated_data['address']['state'],
            zip_code=validated_data['address']['zip_code'],
            country=validated_data['address']['country'],
        )

        #print(f"MemberSerializer.create - validated data : {validated_data}")
        #print(f"MemberSerializer.create - validated data address : {validated_data['address']}")
        #print(f"MemberSerializer.create - validated data categories : {validated_data['categories']}")
        #print(f"MemberSerializer.create - validated data categories[0].name : {validated_data['categories'][0].name}")

        category = validated_data['categories'][0]

        member = Member(
            aft_id=validated_data['aft_id'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            email=validated_data['email'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate'],
            phone_number=validated_data['phone_number'],
            annual_fee_paid=validated_data['annual_fee_paid'],
            is_staff=False,
            is_superuser=False,
            is_active=True,
            address=address

        )



        member.set_password(validated_data['password'])

        # Address must saved first. Address.id requires by Member instance
        address.save()
        # Member.id is required by ManyToMany relationship with Category
        member.save()

        #
        for category in validated_data['categories']:
            member.categories.add(category)

        member.save()

        return member

    def update(self, instance: Member, validated_data):
        print(f"MemberSerializer.update - validated data : {validated_data}")
        print(f"MemberSerializer.update - instance : {instance}")


        if instance.aft_id != validated_data.get('aft_id'):
            raise serializers.ValidationError("Unable to update the instance! Ids doesn't match.")

        # Extract member_ranks from
        member_ranks_data = validated_data.pop('member_ranks_entries', [])

        if settings.DEBUG:
            self.__logger.warning(f"\nMemberSerializer.update - Member_ranks_data : {member_ranks_data}\n")


        address_serializer = AddressSerializer(instance=instance.address, data=validated_data['address'])
        address_serializer.is_valid(raise_exception=True)

        if settings.DEBUG:
            self.__logger.warning(f"MemberSerializer.update - address_serializer.validated_data : {address_serializer.validated_data}")

        address_serializer.save()

        if settings.DEBUG:
            self.__logger.warning(f"MemberSerializer.update - address_serializer.data : {address_serializer.data}")

        instance.email = validated_data.get('email', instance.email)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.annual_fee_paid = validated_data.get('annual_fee_paid', instance.annual_fee_paid)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.address = Address(id=instance.address.id, **address_serializer.validated_data)

        instance.save()

        # Add newest categories
        for category in validated_data['categories']:
            if not instance.categories.filter(pk=category.id).exists():
                instance.categories.add(category)

        instance.save()

        for member_rank_data in member_ranks_data:
            rank = member_rank_data.get("rank")
            points = member_rank_data.get("points")

            MemberRank.objects.update_or_create(
                member=instance,
                rank=rank,
                defaults={"points": points}
            )




        return instance


class MemberWithoutPasswordSerializer(MemberSerializer):
    class Meta:
        model = Member
        fields = [
            'id',
            'aft_id',
            'email',
            'firstname',
            'lastname',
            'gender',
            'birthdate',
            'phone_number',
            'annual_fee_paid',
            'is_superuser',
            'is_staff',
            'is_active',
            'address',
            'categories_ids',
            'categories',
            'member_ranks'
        ]




class MemberDeleteSerializer(serializers.Serializer):
    __logger = logging.getLogger(__name__)
    id = serializers.UUIDField()
    email = serializers.EmailField()
    aft_id = serializers.IntegerField()

    def validate(self, data):
        if settings.DEBUG :
            self.__logger.warning(f"MemberDeleteSerializer.validate - data : {data}")

        member = Member.objects.filter(id=data['id'], aft_id=data['aft_id'], email=data['email'])

        #print(f"MemberDeleteSerializer.validate - member : {member}")

        if member is None:
            raise serializers.ValidationError("ID, AFT ID, or email  is incorrect.")

        data["member"] = member

        return data


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


class MemberReservationSerializer(MemberSerializer):
    class Meta:
        model = Member
        fields = ["aft_id", "email", "firstname", "lastname", "gender", "birthdate", "member_ranks", "categories"]