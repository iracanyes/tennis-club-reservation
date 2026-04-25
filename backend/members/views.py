"""
ViewSets provide CRUD operations in one place.
# ModelViewSet => automatically provides list, retrieve, create, update and destroy actions.
# queryset => defines the set of objects available via the API.
# serializer_class => tells DRF how to serialize/deserialize the Book data.
"""


from rest_framework import viewsets
from members.models import Member
from members.serializers import MemberSerializer

# Create your views here.

