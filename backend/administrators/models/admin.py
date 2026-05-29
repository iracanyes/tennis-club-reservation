#
from members.models import Member


class Admin(Member):
   class Meta:
     app_label = 'tcr_backend'
     db_table = 'admin'
     ordering = ['email']

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['aft_number','firstname', 'lastname', 'birthdate', 'gender', 'phone_number', 'annual_fee_paid', 'address']

   userType = 'admin'

   def __str__(self):
      return f"""Administrator{{
         'id': {self.id},
         'aftId': {self.aft_id},
         'firstname': {self.firstname},
         'lastname': {self.lastname},
         'gender': {self.gender},
         'birthdate': {self.birthdate},
         'phoneNumber': {self.phone_number},
         'email': {self.email},
         'annualFeePaid': {self.annual_fee_paid},
         'address': {self.address},
         'categories': {self.categories},
      }}
      """
