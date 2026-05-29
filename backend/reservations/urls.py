from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourtViewSet, ReservationViewSet

router = DefaultRouter()
router.register('reservations', ReservationViewSet, basename='reservations')
router.register(r'courts', CourtViewSet, basename='courts')

urlpatterns = router.urls