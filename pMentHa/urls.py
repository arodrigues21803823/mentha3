from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patientoverview", views.patientoverview, name="patientoverview"),
    path("regPatient", views.regPatient, name="regPatient"),
    path("test<int:resolutionID>", views.test, name="test"),
    path("teste/pergunta1/<int:testID>-<int:patientID>", views.fazPrimeiraPergunta, name="fazPrimeiraPergunta"),
    path("teste/pergunta<int:order>-<int:resolutionID>", views.fazPergunta, name="fazPergunta"),
    path("report<int:resolutionID>", views.report, name="report")


]
