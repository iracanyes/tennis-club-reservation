# Django Rest Framework 

## ModelViewSet

### Configuration des routes

``DefaultRouter``: Crée les URLs CRUD classiques et une page d'accueil de l'API (Browsable API) répertoriant tous les endpoints
````python from django.urls import path, re_path, include
# members.urls.py
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet

router = DefaultRouter()
router.register(r"mon-endpoint", MemberViewSet, basename="mon-model")


urlpatterns = [
    path('', include(router.urls))
]

````

Pour un ModelViewSet enregistré sous r'items' :
- GET /api/items/ : Liste tous les éléments (.list()).
- POST /api/items/ : Crée un élément (.create()).
- GET /api/items/{id}/ : Récupère un élément (.retrieve()).
- PUT /api/items/{id}/ : Met à jour un élément (.update()).
- DELETE /api/items/{id}/ : Supprime un élément (.destroy())