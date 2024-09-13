from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OverlandView


urlpatterns = [
    path("overland/", OverlandView.as_view(), name="overland"),
]
