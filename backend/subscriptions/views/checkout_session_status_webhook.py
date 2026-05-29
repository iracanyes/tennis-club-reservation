import os
import stripe
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from subscriptions.services.stripe_service import StripeService


class CheckoutSessionStatusWebhook(APIView):
    permission_classes = []
    serializer_class = None
    __logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        stripeSecretKey = os.environ.get("STRIPE_SECRET_KEY")
        self.__stripeWebhookSecretKey = os.environ.get("STRIPE_WEBHOOK_SECRET_KEY")

        if stripeSecretKey is None:
            raise APIException(detail="Stripe read payment key  not set")

        if self.__stripeWebhookSecretKey is None:
            raise APIException(detail="Stripe webhook secret secret key not set")

        self.stripe_client = stripe.StripeClient(stripeSecretKey)
        self.stripe_service = StripeService()

    @csrf_exempt
    def post(self, request):

        # sig header can be found in 2 way :
        # request.headers.get('stripe-signature')
        # request.META.get('HTTP_STRIPE_SIGNATURE')
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        if self.__stripeWebhookSecretKey is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Stripe webhook secret key  not set"})

        if settings.DEBUG :
            self.__logger.warning(f"CheckoutSessionStatusWebhook.post - self.__stripeWebhookSecretKey : {len(self.__stripeWebhookSecretKey) >  0}")
            self.__logger.warning(f"CheckoutSessionStatusWebhook.post - sig_header : {sig_header}")


        try:
            # !!Attention!!
            # construct_event() requires request.body stream
            # which must be used before any use of request.data
            # since request.data requires processing the stream of request.body
            event = self.stripe_client.construct_event(payload=request.body, sig_header=sig_header, secret=self.__stripeWebhookSecretKey)
        except ValueError as e:
            # Invalid payload
            if settings.DEBUG :
                self.__logger.error(f"CheckoutSessionStatusWebhook ValueError : \n{e}")

            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            if settings.DEBUG :
                self.__logger.error(f"CheckoutSessionStatusWebhook stripe.error.SignatureVerificationError : {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


        if(
            event["type"] == "checkout.session.completed"
            or event["type"] == "checkout.session.async_payment_succeeded"
        ):

            self.stripe_service.fulfill_checkout(event['data']['object']['id'])

        return Response(status=status.HTTP_200_OK)