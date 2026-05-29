import logging
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from administrators.models import Admin


class AdminBackend(ModelBackend):
    __logger = logging.getLogger(__name__)

    """
    Authenticate administrators with their email addresses
    """
    def authenticate(self, request, email=None, password=None, **extra_fields):

        if settings.DEBUG == True :
            self.__logger.warning(f"AdminBackend.authenticate arguments : {{ email = {email}, password = {password}, extra_fields = {extra_fields} }}")

        try:
            admin = Admin.objects.get(email=email)

            if settings.DEBUG == True:
                self.__logger.warning(f"AdminBackend.authenticate arguments - admin : {admin}")


            if not admin.check_password(password) or not admin.is_staff or not self.user_can_authenticate(admin):
                raise Admin.DoesNotExist

            return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            member = Admin.objects.get(email=email)
            return member
        except Admin.DoesNotExist:
            return None