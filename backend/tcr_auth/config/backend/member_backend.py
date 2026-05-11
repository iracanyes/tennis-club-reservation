from django.contrib.auth.backends import ModelBackend
from members.models import Member

class MemberBackend(ModelBackend):
    """
    Authenticate members by their aft_id
    """
    def authenticate(self, request, aft_id=None, password=None, **extra_fields):

        #print(f"MemberBackend.authenticate - arguments : {{ aft_id = {aft_id}, password = {password}, extra_fields = {extra_fields} }}")

        try:
            member = Member.objects.get(aft_id=aft_id)

            if member.check_password(password) and self.user_can_authenticate(member) :
                return member
        except Member.DoesNotExist:
            return None

    def get_user(self, aft_id):
        try:
            member = Member.objects.get(aft_id=aft_id)
            return member
        except Member.DoesNotExist:
            return None