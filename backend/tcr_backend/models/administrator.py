#
from . import Member


class Administrator(Member):
   class Meta:
      db_table = 'administrator'

   userType = 'admin'

   def __str__(self):
      return f"""Administrator{{
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
