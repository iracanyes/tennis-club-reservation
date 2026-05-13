from django.contrib.auth import authenticate
from rest_framework import serializers
from members.models import Member, Address, Category
from members.serializers import AddressSerializer


class MemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Member
        fields = ['id','aft_id', 'email', 'password', 'firstname', 'lastname', 'gender', 'birthdate', 'phone_number', 'annual_fee_paid', 'is_superuser', 'is_staff', 'is_active', 'address', 'categories']
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

    def update(self, instance, validated_data):
        print(f"MemberSerializer.update - validated data : {validated_data}")
        print(f"MemberSerializer.update - instance : {instance}")


        if instance.aft_id != validated_data.get('aft_id'):
            raise serializers.ValidationError("Unable to update the instance! Ids doesn't match.")


        address_serializer = AddressSerializer(instance=instance.address, data=validated_data['address'])
        address_serializer.is_valid(raise_exception=True)

        print(f"MemberSerializer.update - address_serializer.validated_data : {address_serializer.validated_data}")

        address_serializer.save()   

        print(f"MemberSerializer.update - address_serializer.data : {address_serializer.data}")

        instance.email = validated_data.get('email', instance.email)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.annual_fee_paid = validated_data.get('annual_fee_paid', instance.annual_fee_paid)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.address = Address(id=instance.address.id, **address_serializer.validated_data)

        instance.save()

        #
        for category in validated_data['categories']:
            if not instance.categories.filter(pk=category.id).exists():
                instance.categories.add(category)

        instance.save()

        return instance


class MemberWithoutPasswordSerializer(MemberSerializer):
    class Meta:
        model = Member
        fields = ['id','aft_id', 'email', 'firstname', 'lastname', 'gender', 'birthdate', 'phone_number', 'annual_fee_paid', 'is_superuser', 'is_staff', 'is_active', 'address', 'categories']




class MemberDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields=["id", "aft_id", "email"]

    def validate(self, data):
        #print(f"MemberDeleteSerializer.validate - data : {data}")

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

