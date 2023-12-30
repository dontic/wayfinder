from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()


urlpatterns = [
    path("overland/", views.OverlandView.as_view()),
    path("visits/", views.VisitsView.as_view(), name="visits"),
    path("visitsplot/", views.VisitsPlotView.as_view(), name="visitsplot"),
]

urlpatterns = router.urls + urlpatterns
