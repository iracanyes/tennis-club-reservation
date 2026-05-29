import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

from members.managers import UserManager
from . import Address, Category, Rank

member_aft_number_validator = RegexValidator(
  regex=r'^[0-9]\d{6}$',
  message='Member aft ID must be between 1000000 and 9999999',
  code='invalid'
)


class Member(AbstractUser):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'member'
    ordering = ['-lastname','-firstname']
    constraints = [
      models.UniqueConstraint(fields=['email'], name='unique_email'),
      models.UniqueConstraint(fields=['aft_id'], name='unique_aft_id'),
    ]

  USERNAME_FIELD = 'aft_id'
  #EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['email','firstname', 'lastname','birthdate','gender', 'phone_number', 'annual_fee_paid', 'address']

  objects = UserManager()

  # Disable all AbstractUser fields not need
  username = None
  first_name = None
  last_name = None

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  aftId = models.CharField(name='aft_id', verbose_name='Identifiant AFT', max_length=7, unique=True, validators=[member_aft_number_validator])
  firstname = models.CharField(max_length=50)
  lastname = models.CharField(max_length=50)
  gender = models.CharField(max_length=1)
  birthdate = models.DateField()
  phoneNumber = models.CharField(name='phone_number', max_length=20)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  annualFeePaid = models.BooleanField(name='annual_fee_paid', default=False)
  userType = 'member'

  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(default=None, null=True, blank=True)

  # Relationships
  # to access address's residents : address.residents
  address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='residents')
  categories = models.ManyToManyField(Category, related_name='members')
  ranks = models.ManyToManyField(Rank, through="MemberRank")





  def __str__(self):
    return f"""{{
      'id': {self.id},
      'aftId': {self.aft_id},
      'firstname': {self.firstname},
      'lastname': {self.lastname},
      'gender': {self.gender},
      'birth_date': {self.birthdate},
      'phone_number': {self.phone_number},
      'email': {self.email},
      'annualFeePaid': {self.annual_fee_paid},
      'address': {self.address},
      'categories': {self.categories},
    }}
    """
