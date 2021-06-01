from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
    })


def mentha_care(request):
    return render(request, "pMentHa/mentha-care.html", {
    })


def login_(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        emailCheck = User.objects.filter(username=username)
        if emailCheck:
            if not user:
                return render(request, "pMentHa/login.html", {
                    "message": "Palavra-Pass inválida."
                })
            else:
                # Check if authentication successful
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "pMentHa/login.html", {
                "message": "Username Inválido"
            })
    else:
        return render(request, "pMentHa/login.html")


def logout_(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "pMentHa/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "pMentHa/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "pMentHa/register.html")


def patientoverview(request):
    return render(request, "pMentHa/patientoverview-novo.html", {
        "patients": Patient.objects.all(),
        "tests": Test.objects.all(),
        "reports": Report.objects.all(),
        "testes": criaTabelaTestes()
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
        return render(request, 'pMentHa/patientoverview-novo.html', {
            "patients": Patient.objects.all(),
            "tests": Test.objects.all(),
            "reports": Report.objects.all(),
            "testes": criaTabelaTestes()
        })
    else:

        return render(request, 'pMentHa/regPatient.html', {
        })


def fazPergunta(request, resolutionID, questionID):
    if request.method == "POST":
        quotation = 0
        answer = Answer.objects.filter(question=questionID, resolution=resolutionID)
        if answer:
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
        questionCount = len(QuestionOrder.objects.filter(test=testID))  # verse len funciona
        order = QuestionOrder.objects.get(test=testID, question=questionID).order

        if order < questionCount:  # se order não for a ultima...
            question = QuestionOrder.objects.get(test=testID, order=order + 1).question
        else:
            # Teste Finalizado, regressar a tabela geral
            return redirect('patientoverview')
        options = Option.objects.filter(question=question.id)
        if question.multipla:
            return render(request, "pMentHa/perguntas/multipla.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "options": options,
                "order": order + 1
            })
        else:
            return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "order": order + 1
            })



def fazPrimeiraPergunta(request, testID, patientID):
    """Esta função é chamada quando na tabela se inicia um teste """
    #Implementar o test.statement antes da primeira pergunta
    question = QuestionOrder.objects.get(test=testID, order=1).question
    options = Option.objects.filter(question=question.id)
    patientInstance = Patient.objects.get(pk=patientID)
    testInstance = Test.objects.get(pk=testID)
    resolution = resolution_exists(patientInstance, testInstance)
    #alterar o if resolution
    if resolution:
        return render(request, "pMentHa/patientoverview-novo.html", {
            "patients": Patient.objects.all(),
            "tests": Test.objects.all(),
            "reports": Report.objects.all(),
            "testes": criaTabelaTestes()
        })
    else:
        resolution = Resolution.objects.create(test=testInstance, patient=patientInstance)
        addTest(testID, patientID)
        if question.multipla:
            return render(request, "pMentHa/perguntas/multipla.html", {
                "question": question,
                "resolutionID": resolution.id,  # permite identificar patient e test
                "options": options,
                "order": 1
            })
        else:
            return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                "question": question,
                "resolutionID": resolution.id,  # permite identificar patient e test
                "order": 1
            })


def report(request, testID, patientID):
    resolutionID = Resolution.objects.get(test=testID, patient=patientID)
    report = report_exists(resolutionID)
    question = QuestionOrder.objects.get(test=testID, order=1).question
    answer = Answer.objects.get(resolution=resolutionID, question=question.id)
    print(report)
    return render(request, "pMentHa/report.html", {
       # "questionsList": questionsAwnsers(resolutionID, testID),
        "advisor": Test.objects.get(pk=testID).advisor.name,
        "question": question,
        "answer": answer
    })
