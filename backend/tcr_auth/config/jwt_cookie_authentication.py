import logging

from django.conf import settings
from rest_framework.authentication import CSRFCheck
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from .csrf_permission_denied_error import CSRFPermissionDeniedError


class JWTCookieAuthentication(JWTAuthentication):
    __logger = logging.getLogger(__name__)

    def authenticate(self, request: Request):
        header = self.get_header(request)

        #print(f"JWTCookieAuthentication - authenticate : header: {header}")

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS"]) or None
        else:
            raw_token = self.get_raw_token(header)
            

        # Add CSRF validation to the Authentification class
        if settings.SIMPLE_JWT["AUTH_COOKIE_USE_CSRF"]:
            self.enforce_csrf(request)


        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        if settings.DEBUG :
            self.__logger.debug(f"JWTCookieAuthentication.authenticate : validated_token: {validated_token}")


        return self.get_user(validated_token), validated_token


    def enforce_csrf(self, request):
        def dummy_get_response(_):
            return None

        check = CSRFCheck(dummy_get_response)

        check.process_request(request)
        reason = check.process_view(request, None, (), {})

        if settings.DEBUG:
            self.__logger.debug(f"JWTCookieAuthentication - enforce_csrf : reason: {reason}")

        if reason:
            raise CSRFPermissionDeniedError(f"CSRF Failed: {reason}")