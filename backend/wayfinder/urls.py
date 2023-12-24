from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path("overland/", views.OverlandView.as_view()),
]

urlpatterns = router.urls + urlpatterns
