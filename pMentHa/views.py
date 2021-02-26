from django.shortcuts import render
from .models import Test, Report, Patient


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
        "test": Test.objects.all(),
        "report": Report.objects.all(),
        "patient": Patient.objects.all()
    })


def evaluation(request, test_id):
    evaluation = Test.objects.get(pk=test_id)
    return render(request, "pMentHa/evaluation.html", {
        "evaluation": evaluation,
        "questions": evaluation.questions.all()
    })
