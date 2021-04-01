from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patientoverview", views.patientoverview, name="patientoverview"),
    path("regPatient", views.regPatient, name="regPatient"),
    path("<int:testID>", views.test, name="test"),
    path("<int:testID>-<int:patientID>", views.fazPrimeiraPergunta, name="fazPrimeiraPergunta"),
    path("asdl<int:testID>-<int:patientID>", views.fazPergunta, name="fazPergunta"),


]
