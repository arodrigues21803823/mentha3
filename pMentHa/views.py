from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
    })


def patientoverview (request):

    return render(request, "pMentHa/patientoverview.html", {
        "patients": Patient.objects.all(),
        "tests": Test.objects.all(),
        "reports": Report.objects.all(),
        "contador": create_table()

    })


def test(request, test_id):
    evaluation = Test.objects.get(pk=test_id)
    return render(request, "pMentHa/test.html", {
        "evaluation": evaluation,
        "questions": evaluation.questions.all(),
    })


def regPatient(request):
    if request.method == "POST":

        email = request.POST["email"]
        gender = request.POST["gender"]
        nacionality = request.POST["nacionality"]
        birth = request.POST["date"]
        disease = request.POST["disease"]
        disease2 = request.POST["disease2"]
        number = request.POST["number"]
        patient = Patient.objects.create(name=request.POST["firstname"],
                                         email=email,
                                         gender=gender, nacionality=nacionality, date=birth, disease=disease, disease2=disease2, number=number)
        patient.save()
        return render(request, 'pMentHa/regPatient.html', {
        })
    else:
        return render(request, 'pMentHa/regPatient.html', {

        })



