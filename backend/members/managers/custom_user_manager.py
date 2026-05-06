"""
Custom UserManager class.
"""

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_superuser(self, aft_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('Email is required.')

        if not extra_fields.get('is_staff') :
            raise ValueError('Superuser must have is_staff=True.')

        extra_fields["email"] = self.normalize_email(email)

        # Prevent error => ValueError: Cannot assign "UUID('dc456002-b754-4ec1-842f-96a691705dcd')": "Member.address" must be an "Address" instance.
        # For foreign keys, the command "python manage.py createsuperuser" ask the primary key field of the address
        # but self.model accept :
        #   - a primary key using the field name in db as positional argument
        #   - or key word argument must contain the object
        # Here,
        address_id = extra_fields["address"]
        extra_fields["address"] = None

        # Prevent error => TypeError: Member() got both positional and keyword arguments for field 'is_superuser'.
        # Remove is_superuser from keyword arguments as it is also passed as positional argument
        extra_fields.pop('is_superuser', None)

        admin = self.model(aft_id=aft_id,  is_superuser=True, address_id=address_id, **extra_fields)

        admin.set_password(password)

        admin.save()

        return admin

    def create_admin(self, aft_id, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)

        extra_fields['email'] = self.normalize_email(email)

        admin = self.model(
            aft_id=aft_id,
            is_staff=True,
            **extra_fields
        )

        admin.set_password(password)
        admin.save()

        return admin


    def create_member(self, aft_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        extra_fields["email"] = self.normalize_email(extra_fields.get('email'))

        address_id = extra_fields["address"]
        extra_fields["address"] = None

        is_superadmin = extra_fields.get('is_superuser')
        extra_fields.pop('is_superuser', None)

        member = self.model(aft_id=aft_id,is_superuser=False,  address_id=address_id, **extra_fields)

        member.set_password(password)

        member.save()

        return member