from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("patientoverview", views.patientoverview, name="patientoverview"),
    path("mentha-care", views.mentha_care, name="mentha-care"),
    path("cog", views.cog, name="cog"),
    path("protocolo", views.protocolo, name="protocolo"),
    path("register", views.register, name="register"),
    path("Registo", views.regPatient, name="regPatient"),
    path("Teste<int:testID>-Paciente<int:patientID>", views.fazPrimeiraPergunta, name="fazPrimeiraPergunta"),
    path("Resolucao<int:resolutionID>-Questao<int:questionID>", views.fazPergunta, name="fazPergunta"),
    path("Resolucao<int:resolutionID>--Questao<int:questionID>", views.prevPergunta, name="prevPergunta"),
    path("Report<int:testID>-<int:patientID>", views.firstReportQuestion, name="firstReportQuestion"),
    path("Report<int:resolutionID>--Questao<int:questionID>", views.reportnextQuestion, name="reportnextQuestion"),
    path("Report<int:resolutionID>---Questao<int:questionID>", views.reportPrevQuestion, name="reportPrevQuestion"),
    path("contacts", views.contact, name="contact"),
    path("patient-summary<int:patientID>", views.patient_summary, name="patientSummary"),
    #Django Auth

    path("login_", views.login_, name="login_"),
    path("logout_", views.logout_, name="logout_")
]

