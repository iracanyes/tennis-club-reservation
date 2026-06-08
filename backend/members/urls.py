from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter


from .views import MemberViewSet, CategoryViewSet, RankViewSet

router = DefaultRouter()
router.register(r"members", MemberViewSet, basename="members")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register("ranks", RankViewSet, basename="ranks")


urlpatterns = router.urls