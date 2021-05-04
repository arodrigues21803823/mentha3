from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
    })


def patientoverview(request):
    return render(request, "pMentHa/patientoverview-novo.html", {
        "patients": Patient.objects.all(),
        "tests": Test.objects.all(),
        "reports": Report.objects.all(),
        "testes": criaTabelaTestes()
    })


def test(request, testID):
    evaluation = Test.objects.get(pk=testID)
    if request.method == "POST":
        awnser = Answer.objects.create(text=request.POST["awnser"], question=request.POST["question_id"], quotation=0,
                                       resolution=1)
        awnser.save()
        return render(request, "pMentHa/test.html", {
            "evaluation": evaluation,
            "questions": evaluation.questions.all(),
        })
    else:
        return render(request, "pMentHa/test.html", {
            "evaluation": evaluation,
            "questions": evaluation.questions.all(),
        })


def regPatient(request):
    if request.method == "POST":
        gender = request.POST["gender"]
        nacionality = request.POST["nacionality"]
        birth = request.POST["date"]
        disease = request.POST["disease"]
        disease2 = request.POST["disease2"]
        number = request.POST["number"]
        patient = Patient.objects.create(name=request.POST["firstname"],
                                         email=request.POST["email"],
                                         gender=gender, nacionality=nacionality,
                                         date=birth, disease=disease,
                                         disease2=disease2, number=number)
        patient.save()
        return render(request, 'pMentHa/regPatient.html', {
        })
    else:
        return render(request, 'pMentHa/regPatient.html', {

        })


def fazPergunta(request, resolutionID, order):
    resolution = Resolution.objects.get(pk=resolutionID)
    question = QuestionsPosition.objects.get(test=resolution.test.id)
    if request.method == "POST":
        quotation = 0
        answer = Answer.objects.filter(question=questionID, resolution=resolutionID)
        if answer is not None:
            # apenas altera a resposta
            answer.text = request.POST["resposta"]
            answer.save()
        else:
            answer = Answer.objects.create(
                text=request.POST["resposta"],
                quotation=quotation,
                question=Question.objects.get(pk=questionID),
                resolution=Resolution.objects.get(pk=resolutionID),
            )
            answer.save()
        testID = Resolution.objects.get(pk=resolutionID).test.id
        print(testID)

        #### CODIGO A EXPERIMENTAR ###

        numero_perguntas_do_teste = len(QuestionsOrder.objects.get(test=testID))  # verse len funciona

        order = QuestionsOrder.objects.get(test=testID, question=questionID).order  # ver se .order funciona
        if order < numero_perguntas_do_teste:  # se order não for a ultima...
            questionID = QuestionsOrder.objects.get(test=testID, order=order + 1).questionID
        else:
            # Teste Finalizado, regressar a tabela geral
            return redirect('patientoverview')

    question = Question.objects.get(pk=questionID)

    return render(request, "pMentHa/pergunta.html", {
        "fileName": 'pMentHa\\perguntas\\' + question.htmlFileName,
        "questionID": questionID,
        "resolutionID": resolutionID  # permite identificar patient e test
    })


def fazPrimeiraPergunta(request, testID, patientID):
    # Esta função é chamada quando na tabela se inicia um teste
    question = QuestionsPosition.objects.get(test=testID, order=1)
    patientInstance = Patient.objects.get(pk=patientID)
    testInstance = Test.objects.get(pk=testID)
    resolution = Resolution.objects.create(test=testInstance, patient=patientInstance)
    question = Question.objects.get(pk=question.question)

    return render(request, "pMentHa/pergunta.html", {
        "fileName": 'pMentHa\\perguntas\\' + question.htmlFileName,
        "questionID": question.id,
        "resolutionID": resolution.id  # permite identificar patient e test
    })


def report(request, resolutionID):
    return render(request, "pMentHa/createReport.html")
