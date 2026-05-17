import os
import stripe
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from subscriptions.serializers import CheckoutSessionSerializer


class CheckoutSessionAPIView(APIView):
    serializer_class = CheckoutSessionSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()

        stripeSecretKey = os.environ.get('STRIPE_SECRET_KEY')

        if stripeSecretKey is None:
            raise Exception('Environment variable STRIPE_SECRET_KEY not set')

        self.__stripe_client = stripe.StripeClient(stripeSecretKey)

    def post(self, request):
        print(f"CheckoutSessionAPIView.post() - request.data: {request.data}")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan = serializer.validated_data['plan']

        print(f"CheckoutSessionAPIView.post() - plan: {plan}")

        try:
            checkout_session = self.__stripe_client.v1.checkout.sessions.create(params={
                'customer_email' : request.user.email,
                'line_items': [
                    {
                        'price': plan.price_id,
                        'quantity': 1,
                    }
                ],
                'mode': 'subscription',
                'success_url' : os.environ.get('STRIPE_CHECKOUT_SESSION_SUCCESS_URL'),
                'cancel_url' : os.environ.get('STRIPE_CHECKOUT_SESSION_CANCEL_URL')
            })



        except Exception as e:
            raise APIException(detail=str(e))

        #print(f"CheckoutSessionAPIView.post() - checkout_session: {checkout_session}")


        return Response(status=status.HTTP_201_CREATED, data={ 'url' : checkout_session.url })