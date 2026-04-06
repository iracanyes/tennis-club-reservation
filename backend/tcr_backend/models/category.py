import uuid
from django.db import models

class Category(models.Model):
  class Meta:
    db_table = 'category'
    ordering = ['name']
    constraints = [
      models.UniqueConstraint(fields=['name'], name='unique_name'),
    ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=50)
  description = models.TextField()
  ageMin = models.IntegerField(null=True)
  ageMax = models.IntegerField(null=True)
  birthYearMin = models.IntegerField(null=True)
  birthYearMax = models.IntegerField( null=True)
  gender = models.CharField(max_length=1)

  parentCategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subCategories')

  def __str__(self):
    return f"""
    {{
      'id' : {self.id},
      'name': {self.name},
      'ageMin' : {self.ageMin},
      'ageMax' : {self.ageMax},
      'birthYearMin' : {self.birthYearMin},
      'birthYearMax' : {self.birthYearMax},
      'gender' : {self.gender},
      'description': {self.description}
    }}
    """