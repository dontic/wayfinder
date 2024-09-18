# urls.py

# Django
from django.urls import path, include

# REST Framework
from rest_framework.routers import DefaultRouter

# Local App
from .views import OverlandView, LocationViewSet, VisitViewSet


urlpatterns = [path("overland/", OverlandView.as_view(), name="overland")]

router = DefaultRouter()
router.register(r"locations", LocationViewSet)
router.register(r"visits", VisitViewSet)

urlpatterns += [
    path("", include(router.urls)),
]
