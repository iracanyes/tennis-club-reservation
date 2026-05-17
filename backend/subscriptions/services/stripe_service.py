import os
from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from stripe import StripeClient
from members.models import Member
from subscriptions.models import Payment, Subscription, Plan


class StripeService:
    Instance = None

    def __init__(self):
        if os.environ.get("STRIPE_READ_PAYMENT_KEY") is None:
            raise APIException("Stripe secret key not set")

        self.client = StripeClient(os.environ.get("STRIPE_READ_PAYMENT_KEY"))

   # Singleton pattern
    def __new__(cls):
        if cls.Instance is None:
            cls.Instance = super().__new__(cls)

        return cls.Instance


    def fulfill_checkout(self, session_id: str):
        """
        Method to fulfill the Stripe checkout payment session after successful payment
        Used by the Stripe webhook endpoint to push notifications.on Checkout session status
        """

        # TODO: Make this function safe to run multiple times,
        # even concurrently, with the same session ID

        # TODO: Make sure fulfillment hasn't already been
        # performed for this Checkout Session
        print(f"FulFilling Checkout session - id : {session_id}")

        try:
            payment = Payment.objects.get(checkout_session_id=session_id)

            print(f"FulFilling Checkout session - payment : {payment}")

            # If a payment is already registered for the checkout session, return OK
            if payment is not None and payment.payment_status in ['paid']:
                return Response(status=status.HTTP_200_OK)
        except Payment.DoesNotExist as e:
            print(f"FulFilling Checkout session - retrieve payment exception : \n{e}")

        # Retrieve the Checkout Session from the Stripe API with line_items expanded
        checkout_session = self.client.v1.checkout.sessions.retrieve(
            session_id,
            params={'expand':['line_items','customer_details']},
        )

        # Check the Checkout Session's payment_status property
        # to determine if fulfillment should be performed
        if checkout_session.payment_status != 'unpaid':
            if checkout_session.customer_email is None:
                raise APIException(f"StripeService.fulfill_checkout failed :- customer_email not set")

            try:
                # TODO: Perform fulfillment of the line items
                member = Member.objects.get(email=checkout_session.customer_email)

                if member is None:
                    raise APIException("StripeService.fulfill_checkout failed : member doesn't exists.")

                # TODO: Record/save fulfillment status for this
                # Retrieve plan
                plan = Plan.objects.get(product_id=checkout_session.line_items.data[0].price.product)

                if plan is None:
                    raise APIException("StripeService.fulfill_checkout failed : plan not found by its product ID.")

                # Create & save a payment

                payment = Payment(
                    checkout_session_id=checkout_session.id,
                    created_at=datetime.fromtimestamp(checkout_session.created),
                    expired_at=datetime.fromtimestamp(checkout_session.expires_at),
                    payment_status=checkout_session.payment_status,
                    status = checkout_session.status,
                    amount_total=checkout_session.amount_total / 100,
                    amount_subtotal=checkout_session.amount_subtotal / 100,
                    currency=checkout_session.currency,
                )

                # Register a subscription
                subscription = Subscription(
                    date_created=datetime.now(),
                    year=datetime.today().year,
                    fee=checkout_session.amount_total / 100,
                    paid_in_cash=False,
                    reference=checkout_session.id,
                    member=member,
                )

                # Save the subscription
                subscription.save()

                payment.plan = plan
                payment.subscription = subscription
                payment.save()

                # Unlock the member
                member.annualFeePaid = True
                member.save()
            except Exception as e:
                raise APIException(f"StripeService.fulfill_checkout failed :- \n{e}")

            return Response(status=status.HTTP_200_OK)
