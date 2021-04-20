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
        awnser = Answer.objects.create(text=request.POST["awnser"], question=request.POST["question_id"], quotation=0, resolution=1)
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
                                         gender=gender, nacionality=nacionality, date=birth, disease=disease,
                                         disease2=disease2, number=number)
        patient.save()
        return render(request, 'pMentHa/regPatient.html', {
        })
    else:
        return render(request, 'pMentHa/regPatient.html', {

        })


def fazPergunta(request, resolutionID, questionID):

    if request.method == "POST":
        text = request.POST["resposta"]
        quotation = 0 # request.POST["quotation"]

        # e se já existir uma resposta para essa (question,resolution,patient) e se resubmeter?
        # cria-se novo objeto ou altera-se? verificamos primeiro se existe? verificar o q acontece...
        # podiamos ter algo do genero:
        # avaliar se usar filter ou get. verificar que, se não existe, retorna None. é isso que nos interessa.
        answer = Answer.objects.filter(question=questionID, resolution=resolutionID)
        if answer is not None:
            # apenas altera a resposta
            answer.text = request.POST["resposta"]
            answer.save()
        else:
            answer = Answer.objects.create(
                text=text,
                quotation=quotation, # ? fica para mais tarde? ou  no formulario há campo "quotation" para além
                                # da resposta em si? se sim, a pergunta tem que ter input com name="quotation"
                                # nesse caso podemos por como regra que todas as perguntas (p1.html) tenham um campo
                                # <input name="quotation">, que pode ter valor especificado, ou ser hidden com valor None (caso não se dê cotação)
                                # ver os formularios e verificar se estes campos são suficientes, text e quotation
                question=Question.objects.get(pk=questionID),
                resolution=Resolution.objects.get(pk=resolutionID),
            )
            answer.save()
        print("\n\n\n\n\n\n\nVou gerar um testID\n\n\n\n\n\n\n\n\n")
        testID = Resolution.objects.get(pk=resolutionID).test.id
        print(testID)
        questionID = proximaPergunta(testID, questionID)

    if questionID == -1:
        #Teste Finalizado, regressar a tabela geral
        return redirect('patientoverview')

    question = Question.objects.get(pk=questionID)
    #HTMLPergunta=constroiTextoPergunta(resolutionID, question)

    return render(request, "pMentHa/pergunta.html", {
            "fileName": 'pMentHa\\perguntas\\' + question.htmlFileName,
            "questionID": questionID,
            "resolutionID": resolutionID # permite identificar patient e test
        })

def fazPrimeiraPergunta(request, testID, patientID):
    """Esta função é chamada quando na tabela se inicia um teste """
    patientInstance = Patient.objects.get(pk=patientID)
    testInstance = Test.objects.get(pk=testID)
    resolution = Resolution.objects.create(test=testInstance, patient=patientInstance)
    question = Question.objects.get(pk=proximaPergunta(testID, 0))
    #HTMLPergunta = constroiTextoPergunta(resolution.id, question)

    return render(request, "pMentHa/pergunta.html", {
            "fileName": 'pMentHa\\perguntas\\' + question.htmlFileName,
            "questionID": question.id,
            "resolutionID": resolution.id # permite identificar patient e test
        })

def report(request, resolutionID):
    return render(request, "pMentHa/createReport.html")