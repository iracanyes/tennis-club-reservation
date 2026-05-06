from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        header = self.get_header(request)

        #print(f"JWTCookieAuthentication - authenticate : header: {header}")

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS"])
        else:
            raw_token = self.get_raw_token(header)

        #print(f"JWTCookieAuthentication - authenticate : raw_token: {raw_token}")


        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        print(f"JWTCookieAuthentication - authenticate : validated_token: {validated_token}")


        return self.get_user(validated_token), validated_token