from django.db import models
import uuid

from django.db.models import Q


class Credential(models.Model):
  class Meta:
    app_label = 'tcr_auth'
    db_table = 'credential'
    verbose_name = 'credential'
    verbose_name_plural = 'credentials'
    constraints = [
      models.UniqueConstraint(fields=['email'], name='credential_unique_email'),
      models.UniqueConstraint(fields=['aft_number'], name='credential_unique_aft_number'),
      models.CheckConstraint(
        condition=Q(aft_number__gte=1000000) & Q(aft_number__lte=9999999),
        name="credential_aft_number_valid"
      ),
    ]

  credential_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  aft_number = models.IntegerField()
  email = models.EmailField(max_length=255, unique=True)
  password = models.CharField(max_length=255)

  googleHash = models.CharField(max_length=255)

  is_staff = models.BooleanField(default=False)
  active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"""
    {{
      'id' : {self.credential_id},
      'aft_number' : {self.aft_number},
      'email' : {self.email},
      'password' : ';-)',
      'googleHash' : {self.googleHash},
      'is_staff' : {self.is_staff},
      'active' : {self.active},
      'created_at' : {self.created_at},
      'updated_at' : {self.updated_at},
    }}
    """