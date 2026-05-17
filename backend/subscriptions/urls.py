from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, CheckoutSessionAPIView, CheckoutSessionStatusWebhook

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plans')

urlpatterns = [
    path( '', include(router.urls)),
    path('payment/checkout_session', CheckoutSessionAPIView.as_view(), name='stripe_checkout_session' ),
    path('webhook/payment/checkout_session', CheckoutSessionStatusWebhook.as_view(), name='webhook_checkout_session' ),
]