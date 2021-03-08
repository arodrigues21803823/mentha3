from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patientoverview", views.patientoverview, name="patientoverview"),
    path("regPatient", views.regPatient, name="regPatient"),
    path("<int:test_id>", views.test, name="test")
]
