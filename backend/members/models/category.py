import uuid
from django.db import models

class Category(models.Model):
  class Meta:
    app_label = 'tcr_backend'
    db_table = 'category'
    ordering = ['name']
    constraints = [
      models.UniqueConstraint(fields=['name'], name='unique_name'),
    ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=50)
  description = models.TextField()
  age_min = models.IntegerField(name='age_min', null=True)
  age_max = models.IntegerField(name='age_max', null=True)
  birth_year_min = models.IntegerField(name='birth_year_min', null=True)
  birth_year_max = models.IntegerField(name='birth_year_max', null=True)
  gender = models.CharField(max_length=1)

  parentCategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subCategories')

  def __str__(self):
    return f"""
    {{
      'id' : {self.id},
      'name': {self.name},
      'ageMin' : {self.age_min},
      'ageMax' : {self.age_max},
      'birthYearMin' : {self.birth_year_min},
      'birthYearMax' : {self.birth_year_max},
      'gender' : {self.gender},
      'description': {self.description}
    }}
    """