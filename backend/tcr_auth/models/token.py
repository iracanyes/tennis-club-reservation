import uuid
from django.db import models

from tcr_auth.models.credential import Credential


class Token(models.Model):
  token_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  token = models.CharField(max_length=255)
  refresh_token = models.CharField(max_length=255)

  credential = models.OneToOneField(Credential, on_delete=models.CASCADE)

  def __str__(self):
    return f"""
    {{
      'id' : {self.token_id},
      'token' : {self.token},
      'refresh_token' : {self.refresh_token},
      'credential' : {self.credential},
    }}
    """