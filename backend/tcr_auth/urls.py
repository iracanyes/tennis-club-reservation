from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView

from .views import (
  MemberLoginAPIView,
  AdminLoginAPIView,
  RefreshTokenAPIView,
  UserRetrieveAPIView,
  LogoutAPIView,
  AdminLoginGoogleAPIView
)

app_name = 'tcr_auth'

router = DefaultRouter()


urlpatterns = [
  path('whoami', UserRetrieveAPIView.as_view(), name='api-whoami'),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair' ),
  path('token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh' ),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify' ),
  path('member/login', MemberLoginAPIView.as_view(), name='member-login'),
  path('admin/login', AdminLoginAPIView.as_view(), name='admin-login'),
  path('admin/login/google', AdminLoginGoogleAPIView.as_view() , name="admin-login-google"),
  path('logout', LogoutAPIView.as_view() , name='logout')

]