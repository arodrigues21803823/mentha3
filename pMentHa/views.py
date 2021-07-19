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


def protocolo(request):
    return render(request, "pMentHa/protocolo.html", {
    })


def cog(request):
    return render(request, "pMentHa/cog.html", {
    })


def image(request, images):
    return render(request, "pMentHa/image.html", {
        "image": images
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
        code = request.POST["code"]
        if code != "0000":
            return render(request, "pMentHa/register.html", {
                "message": "Código MentHA Inválido"
            })
        if password != confirmation:
            return render(request, "pMentHa/register.html", {
                "message": "Palavras-Chave Não Correspondem"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,)
            user.groups.add(name='Staff')
            user.save()
        except IntegrityError:
            return render(request, "pMentHa/register.html", {
                "message": "Nome de Utilizador Já Utilizado"
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


def patient_summary(request, patientID):
    age = 2021 - Patient.objects.get(pk=patientID).date.year
    return render(request, "pMentHa/patient-summary.html", {
        "patient": Patient.objects.get(pk=patientID),
        "tests": Test.objects.all(),
        "age": age,
        "reports": Report.objects.all(),
        "testes": criaTabelaTeste(patientID=patientID)
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


def prevPergunta(request, resolutionID, questionID):
    testID = Resolution.objects.get(pk=resolutionID).test.id
    order = QuestionOrder.objects.get(test=testID, question=questionID).order
    if order > 1:
        question = QuestionOrder.objects.get(test=testID, order=order - 1).question
        order = order - 1
    else:
        question = QuestionOrder.objects.get(test=testID, order=order).question
    options = Option.objects.filter(question=question.id)
    answer = Answer.objects.get(question=question.id, resolution=resolutionID).text
    if question.multipla:
        if question.cover:
            return render(request, "pMentHa/perguntas/multipla.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "options": options,
                "answer": int(answer),
                "order": order,
                "image": question.cover,
                "test": Resolution.objects.get(pk=resolutionID).test.name
            })
        else:
            return render(request, "pMentHa/perguntas/multipla.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "options": options,
                "answer": int(answer),
                "order": order,
                "test": Resolution.objects.get(pk=resolutionID).test.name
            })
    else:
        if question.cover:
            return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "order": order,
                "answer": answer,
                "test": Resolution.objects.get(pk=resolutionID).test.name,
                "image": question.cover
            })
        else:
            return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "order": order,
                "answer": answer,
                "test": Resolution.objects.get(pk=resolutionID).test.name
            })


def fazPergunta(request, resolutionID, questionID):
    if request.method == "POST":
        quotation = 0
        answer = Answer.objects.filter(question=questionID, resolution=resolutionID)
        if answer:
            # apenas altera a resposta
            answer = Answer.objects.get(question=questionID, resolution=resolutionID)
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
        questionCount = len(QuestionOrder.objects.filter(test=testID))
        order = QuestionOrder.objects.get(test=testID, question=questionID).order

        if order < questionCount:
            question = QuestionOrder.objects.get(test=testID, order=order + 1).question
        else:
            # Teste Finalizado, regressar a tabela geral
            patientID = Resolution.objects.get(pk=resolutionID).patient.id
            addTest(testID, patientID)
            return redirect('patientoverview')
        answer = Answer.objects.filter(question=question.id, resolution=resolutionID)
        options = Option.objects.filter(question=question.id)
        if answer:
            answer = Answer.objects.get(question=question.id, resolution=resolutionID).text
            if question.multipla:
                if question.cover:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolutionID,  # permite identificar patient e test
                        "options": options,
                        "answer": int(answer),
                        "order": order + 1,
                        "image": question.cover,
                        "test": Resolution.objects.get(pk=resolutionID).test.name
                    })
                else:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolutionID,  # permite identificar patient e test
                        "options": options,
                        "answer": int(answer),
                        "order": order + 1,
                        "test": Resolution.objects.get(pk=resolutionID).test.name
                    })
            else:
                if question.cover:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolutionID,  # permite identificar patient e test
                        "order": order + 1,
                        "answer": answer,
                        "test": Resolution.objects.get(pk=resolutionID).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolutionID,  # permite identificar patient e test
                        "order": order + 1,
                        "answer": answer,
                        "test": Resolution.objects.get(pk=resolutionID).test.name
                    })

        else:
            if question.multipla:
                if question.cover:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolutionID,
                        "options": options,
                        "order": order + 1,
                        "test": Resolution.objects.get(pk=resolutionID).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolutionID,
                        "options": options,
                        "order": order + 1,
                        "test": Resolution.objects.get(pk=resolutionID).test.name,
                    })
            else:
                if question.cover:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolutionID,  # permite identificar patient e test
                        "order": order + 1,
                        "test": Resolution.objects.get(pk=resolutionID).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolutionID,  # permite identificar patient e test
                        "order": order + 1,
                        "test": Resolution.objects.get(pk=resolutionID).test.name
                    })


def fazPrimeiraPergunta(request, testID, patientID):
    """Esta função é chamada quando na tabela se inicia um teste """
    question = QuestionOrder.objects.get(test=testID, order=1).question
    options = Option.objects.filter(question=question.id)
    patientInstance = Patient.objects.get(pk=patientID)
    testInstance = Test.objects.get(pk=testID)
    resolution = resolution_exists(patientInstance, testInstance)
    if resolution:
        answer = Answer.objects.filter(question=question.id,
                                       resolution=Resolution.objects.get(test=testInstance, patient=patientInstance))
        if answer:
            answer = Answer.objects.get(question=question.id,
                                        resolution=Resolution.objects.get(test=testInstance,
                                                                          patient=patientInstance)).text
            resolution = Resolution.objects.get(patient=patientInstance, test=testInstance)
            if question.multipla:
                print(question.cover)
                if question.cover:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "options": options,
                        "answer": int(answer),
                        "order": 1,
                        "image": question.cover,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
                else:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "options": options,
                        "answer": int(answer),
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
            else:
                if question.cover:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "order": 1,
                        "answer": answer,
                        "image": question.cover,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
                else:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "order": 1,
                        "answer": answer,
                        "test": Resolution.objects.get(pk=resolution.id).test.name
                    })
        else:
            resolution = Resolution.objects.get(patient=patientInstance, test=testInstance)
            if question.multipla:
                if question.cover:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "options": options,
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/multipla.html", {
                        "question": question,
                        "resolutionID": resolution.id,
                        "options": options,
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                    })

            else:
                if question.cover:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                        "image": question.cover
                    })
                else:
                    return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                        "question": question,
                        "resolutionID": resolution.id,  # permite identificar patient e test
                        "order": 1,
                        "test": Resolution.objects.get(pk=resolution.id).test.name,
                    })

    else:
        resolution = Resolution.objects.create(test=testInstance, patient=patientInstance)
        if question.multipla:
            if question.cover:
                return render(request, "pMentHa/perguntas/multipla.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "options": options,
                    "order": 1,
                    "image": question.cover,
                    "test": resolution.test.name
                })
            else:
                return render(request, "pMentHa/perguntas/multipla.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "options": options,
                    "order": 1,
                    "test": resolution.test.name
                })
        else:
            if question.cover:
                return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "order": 1,
                    "image": question.cover,
                    "test": resolution.test.name
                })
            else:
                return render(request, "pMentHa/perguntas/desenvolvimento.html", {
                    "question": question,
                    "resolutionID": resolution.id,  # permite identificar patient e test
                    "order": 1,
                    "test": resolution.test.name
                })


def firstReportQuestion(request, testID, patientID):
    """Esta função é chamada quando na tabela se inicia um teste """
    # Implementar o test.statement antes da primeira pergunta
    question = QuestionOrder.objects.get(test=testID, order=1).question
    options = Option.objects.filter(question=question.id)
    patientInstance = Patient.objects.get(pk=patientID)
    testInstance = Test.objects.get(pk=testID)
    # alterar o if resolution
    answer = Answer.objects.get(question=question.id,
                                resolution=Resolution.objects.get(test=testInstance, patient=patientInstance)).text
    resolution = Resolution.objects.get(patient=patientInstance, test=testInstance)
    if question.multipla:
        if question.cover:
            return render(request, "pMentHa/perguntas/multipla-report.html", {
                "question": question,
                "resolutionID": resolution.id,  # permite identificar patient e test
                "options": options,
                "answer": int(answer),
                "order": 1,
                "image": question.cover,
                "test": Resolution.objects.get(pk=resolution.id).test.name
            })
        else:
            return render(request, "pMentHa/perguntas/multipla-report.html", {
                "question": question,
                "resolutionID": resolution.id,  # permite identificar patient e test
                "options": options,
                "answer": int(answer),
                "order": 1,
                "test": Resolution.objects.get(pk=resolution.id).test.name
            })

    else:
        if question.cover:
            return render(request, "pMentHa/perguntas/desenvolvimento-report.html", {
                "question": question,
                "resolutionID": resolution.id,
                "order": 1,
                "image": question.cover,
                "test": Resolution.objects.get(pk=resolution.id).test.name,
                "answer": answer
            })
        else:
            return render(request, "pMentHa/perguntas/desenvolvimento-report.html", {
                "question": question,
                "resolutionID": resolution.id,
                "order": 1,
                "test": Resolution.objects.get(pk=resolution.id).test.name,
                "answer": answer
            })


def reportnextQuestion(request, resolutionID, questionID):
    if request.method == "POST":
        testID = Resolution.objects.get(pk=resolutionID).test.id
        questionCount = len(QuestionOrder.objects.filter(test=testID))
        order = QuestionOrder.objects.get(test=testID, question=questionID).order

        if order < questionCount:  # se order não for a ultima...
            question = QuestionOrder.objects.get(test=testID, order=order + 1).question
        else:
            # Teste Finalizado, regressar a tabela geral
            patientID = Resolution.objects.get(pk=resolutionID).patient.id
            addTest(testID, patientID)
            return redirect('patientoverview')
        options = Option.objects.filter(question=question.id)
        answer = Answer.objects.filter(question=question.id, resolution=resolutionID)
        if answer:
            answer = Answer.objects.get(question=question.id, resolution=resolutionID).text
        if question.multipla:
            if question.cover:
                return render(request, "pMentHa/perguntas/multipla-report.html", {
                    "question": question,
                    "resolutionID": resolutionID,  # permite identificar patient e test
                    "options": options,
                    "answer": int(answer),
                    "order": order + 1,
                    "test": Resolution.objects.get(pk=resolutionID).test.name,
                    "image": question.cover
                })
            else:
                print(answer)
                return render(request, "pMentHa/perguntas/multipla-report.html", {
                    "question": question,
                    "resolutionID": resolutionID,  # permite identificar patient e test
                    "options": options,
                    "answer": int(answer),
                    "order": order + 1,
                    "test": Resolution.objects.get(pk=resolutionID).test.name,
                })
        else:
            if question.cover:
                return render(request, "pMentHa/perguntas/desenvolvimento-report.html", {
                    "question": question,
                    "resolutionID": resolutionID,  # permite identificar patient e test
                    "order": order + 1,
                    "answer": answer,
                    "image": question.cover,
                    "test": Resolution.objects.get(pk=resolutionID).test.name
                })
            else:
                return render(request, "pMentHa/perguntas/desenvolvimento-report.html", {
                    "question": question,
                    "resolutionID": resolutionID,  # permite identificar patient e test
                    "answer": answer,
                    "order": order + 1,
                    "test": Resolution.objects.get(pk=resolutionID).test.name
                })


def reportPrevQuestion(request, resolutionID, questionID):
    testID = Resolution.objects.get(pk=resolutionID).test.id
    order = QuestionOrder.objects.get(test=testID, question=questionID).order
    if order > 1:
        question = QuestionOrder.objects.get(test=testID, order=order - 1).question
        order = order - 1
    else:
        # Teste Finalizado, regressar a tabela geral
        question = QuestionOrder.objects.get(test=testID, order=order).question
    options = Option.objects.filter(question=question.id)
    answer = Answer.objects.filter(question=question.id, resolution=resolutionID)
    if answer:
        answer = Answer.objects.get(question=question.id, resolution=resolutionID).text
    if question.multipla:
        if question.cover:
            return render(request, "pMentHa/perguntas/multipla-report.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "options": options,
                "answer": int(answer),
                "order": order,
                "test": Resolution.objects.get(pk=resolutionID).test.name,
                "image": question.cover
            })
        else:
            return render(request, "pMentHa/perguntas/multipla-report.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "options": options,
                "answer": int(answer),
                "order": order,
                "test": Resolution.objects.get(pk=resolutionID).test.name
            })

    else:
        if question.cover:
            return render(request, "pMentHa/perguntas/desenvolvimento-report.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "order": order + 1,
                "image": question.cover,
                "test": Resolution.objects.get(pk=resolutionID).test.name
            })
        else:
            return render(request, "pMentHa/perguntas/desenvolvimento-report.html", {
                "question": question,
                "resolutionID": resolutionID,  # permite identificar patient e test
                "order": order + 1,
                "test": Resolution.objects.get(pk=resolutionID).test.name
            })


def contact(request):
    if request.method == "POST":
        contact = Contact.objects.create(email=request.POST["email"],
                                         contact=request.POST["contact"],
                                         name=request.POST["name"], birth=request.POST["date"])
        contact.save()
        return render(request, 'pMentHa/index.html', {
        })

    else:
        return render(request, 'pMentHa/contacts.html', {
        })
