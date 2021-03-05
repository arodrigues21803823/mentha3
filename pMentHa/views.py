from django.shortcuts import render
from .models import Test, Report, Patient


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
    })


def evaluation(request, test_id):
    evaluation = Test.objects.get(pk=test_id)
    return render(request, "pMentHa/evaluation.html", {
        "evaluation": evaluation,
        "questions": evaluation.questions.all()

    })


def overview(request):

    return render(request, "pMentHa/overview.html", {
        "patients": Patient.objects.all()

    })
