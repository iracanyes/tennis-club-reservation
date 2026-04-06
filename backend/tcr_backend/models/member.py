import uuid
from django.db import models
from django.db.models import Q

from . import Address, Category


class Member(models.Model):
  class Meta:
    db_table = 'member'
    ordering = ['-lastname','-firstname']
    constraints = [
      models.UniqueConstraint(fields=['email'], name='unique_email'),
      models.UniqueConstraint(fields=['aftNumber'], name='unique_aft_number'),
      models.CheckConstraint(
        condition=Q(aft_number__gte=1000000) & Q(aft_number__lte=999999),
      ),
    ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  aftNumber = models.IntegerField()
  firstname = models.CharField(max_length=50)
  lastname = models.CharField(max_length=50)
  gender = models.CharField(max_length=1)
  birth_date = models.DateField()
  phone_number = models.CharField(max_length=20)
  email = models.EmailField()
  password = models.CharField(max_length=50)
  annualFeePaid = models.BooleanField(default=False)
  userType = 'member'

  # Relationships
  # to access address's residents : address.residents
  address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='residents')
  categories = models.ManyToManyField(Category, related_name='members')



  def __str__(self):
    return f"""
    {{
      'id': {self.id},
      'aftNumber': {self.aftNumber},
      'firstname': {self.firstname},
      'lastname': {self.lastname},
      'gender': {self.gender},
      'birth_date': {self.birth_date},
      'phone_number': {self.phone_number},
      'email': {self.email},
      'annualFeePaid': {self.annualFeePaid},
      'address': {self.address},
      'categories': {self.categories},
    }}
    """
