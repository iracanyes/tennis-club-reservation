import uuid
from django.db import models

from subscriptions.models import Subscription, Plan


class Payment(models.Model):
    class Meta:
        app_label = 'tcr_backend'
        db_table = 'payment'
        ordering = ['-created_at',]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    checkout_session_id = models.CharField(max_length = 255)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    amount_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length = 5)
    status = models.CharField(max_length = 255)
    payment_status = models.CharField(max_length = 255)

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments', null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='payments')

