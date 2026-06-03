from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourtViewSet, EventViewSet, ReservationViewSet

router = DefaultRouter()
router.register('reservations', ReservationViewSet, basename='reservations')
router.register(r'courts', CourtViewSet, basename='courts')
router.register(r"events", EventViewSet, basename='events')

urlpatterns = router.urls