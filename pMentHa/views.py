from django.shortcuts import render
from .models import Test, Report, Patient, Answer, Question


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
    })


def patientoverview (request):
    return render(request, "pMentHa/patientoverview.html", {
        "patients": Patient.objects.all(),
        "tests": Test.objects.all(),
        "reports": Report.objects.all()

    })

def regPatient(request):
    return render(request, "pMentHa/regPatient.html", {
    })


def test (request, test_id):
    evaluation = Test.objects.get(pk=test_id)
    return render(request, "pMentHa/test.html", {
        "evaluation": evaluation,
        "perguntas": evaluation.questions.all(),
    })
