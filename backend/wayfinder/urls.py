# urls.py

# Django
from django.urls import path, include

# REST Framework
from rest_framework.routers import DefaultRouter

# Local App
from .views import OverlandView, LocationViewSet


urlpatterns = [path("overland/", OverlandView.as_view(), name="overland")]

router = DefaultRouter()
router.register(r"locations", LocationViewSet)

urlpatterns += [
    path("", include(router.urls)),
]
