import uuid
from django.db import models

class Plan(models.Model):
    class Meta:
        app_label = "tcr_backend"
        db_table = "plan"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    summary = models.TextField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=100)
    currency_symbol = models.CharField(max_length=30, blank=True, null=True)
    img_src = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    price_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"""
        {{
            'id' : {self.id},
            'title' : {self.title},
            'subtitle' : {self.subtitle},
            'description' : {self.description},
            'price' : {self.price},
            'currency' : {self.currency}
            'currency_symbol' : {self.currency_symbol}
            'img_src' : {self.img_src},
            'product_id' : {self.product_id},
            'price_id' : {self.price_id},
        }}
        """