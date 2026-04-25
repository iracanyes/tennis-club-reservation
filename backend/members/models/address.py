import uuid
from django.db import models

class Address(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'address'

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  street = models.CharField(max_length=50)
  number = models.CharField(max_length=30)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  zipCode = models.CharField(name='zip_code', max_length=30)
  country = models.CharField(max_length=50)

  def __str__(self):
    return f"""
    {{
      'id':{self.id},
      'street':{self.street},
      'number':{self.number},
      'city':{self.city},
      'state':{self.state},
      'zipCode':{self.zip_code},
      'country':{self.country}
    }}
    """