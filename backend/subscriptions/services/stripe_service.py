import os

from rest_framework.exceptions import APIException
from stripe import StripeClient


class StripeService():
    def __init__(self):
        if os.environ.get("STRIPE_SECRET_KEY") is None:
            raise APIException("Stripe secret key not set")

        self.client = StripeClient(os.environ["STRIPE_SECRET_KEY"])

    def get_payment_link(self, line_items : dict):
        pass