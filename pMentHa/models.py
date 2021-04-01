from django.db import models
from django import forms


# Create your models here.
class Question(models.Model):
    type = models.CharField(max_length=64)
    htmlFileName = models.TextField(max_length=1000)
    quotation = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}:{self.htmlFileName}"


class Test(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    statement = models.TextField(max_length=1000)
    questions = models.ManyToManyField('Question', blank=True, related_name="questions")
    advisor = models.ForeignKey('Advisor', on_delete=models.SET_NULL, null=True, related_name="advisor")

    def __str__(self):
        return f"Teste {self.id}"


class Answer(models.Model):
    text = models.TextField(max_length=258)
    quotation = models.CharField(max_length=64, blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, related_name="respostas")
    resolution = models.ForeignKey('Resolution', on_delete=models.SET_NULL, null=True, related_name="resolution")

    def __str__(self):
        return f"{self.text}"


class Advisor(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    nacionality = models.CharField(max_length=64)
    date = models.DateField()
    disease = models.CharField(max_length=64)
    disease2 = models.TextField(max_length=258, blank=True)
    number = models.IntegerField()
    tests = models.ManyToManyField('Test', blank=True, related_name="tests")
    resolutions = models.ManyToManyField('Resolution', blank=True, related_name="resolutions")

    def __str__(self):
        return f"{self.name}, {self.id}"


class Resolution(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, related_name="patient")
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True, related_name="test")

    def __str__(self):
        return f"{self.id}"

    def returnResolution(self):
        pass


class Report(models.Model):
    resolution = models.ForeignKey('Resolution', on_delete=models.SET_NULL, null=True)
    advisor = models.ForeignKey('Advisor', on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"Relatório do teste {self.resolution.test}: {self.text}"


def criaTabelaTestes():
    testes = []
    for patient in Patient.objects.all():

        dicPaciente = {}

        dicPaciente["nome"] = patient.name
        dicPaciente["id"] = patient.id

        testesFeitos = []
        for test in patient.tests.all():
            testesFeitos.append(test.id)
        dicPaciente["testesFeitos"] = testesFeitos

        if len(testesFeitos) < 5:
            dicPaciente["proximoTesteAFazer"] = [len(testesFeitos) + 1]

        testesPorFazer = []
        if len(testesFeitos) < 5:
            for i in range(len(testesFeitos)+2, 5+1):
                testesPorFazer.append(i)
        dicPaciente["testesPorFazer"] = testesPorFazer

        testes.append(dicPaciente)

    return testes


def constroiTextoPergunta(resolutionID, question):
    #import os

    #caminhoPastaPerguntas = os.getcwd() + "pMentHa\\templates\\pMentHa\\perguntas\\"

    #if not os.path.isdir(caminhoPastaPerguntas):
     #   print("\n\nErro de acesso a pasta de perguntas")

    #os.path.join(caminho, nomeFicheiro)

    caminho = "pMentHa\\templates\\pMentHa\\perguntas\\"
    with open(caminho + question.htmlFileName,  encoding='utf-8') as ficheiro:
        HTMLDaPergunta = ficheiro.read()

        # se uma pergunta já foi respondida e for necessário ve-la novamente
        # (por exemplo, se voltar para tras? ou se o avaliador quiser revisitar o teste)
        # nesse caso já existe answer para o tuplo (question,resolution,pacient).
        # pode-se assim verificar, antes de retornar HTMLDaPergunta, se existe resposta
        # tal como proposto em baixo:

        answer = Answer.objects.filter(question=question.id, resolution=resolutionID)
        if answer != None:
            pass
            # caso exista, deve-se inserir em HTMLDaPergunta a resposta
            # Como as perguntas são de dois tipos:

            #  - nas de desenvolvimento basta inserir um atributo value com valor a resposta.
            #  como? substituindo 'name="resposta"' por 'name="resposta" value="resposta armazenada"'
            #  fica:
            # <input type="text" name="resposta" value="resposta já feita em texto">.
            # proposta de codigo:
            if question.type == "desenvolvimento":
                valueWithAnswer = f'name="resposta" value="{answer.text}"'
                HTMLDaPergunta.replace('name="resposta"', valueWithAnswer)

            #  - nas de opção multipla type="radio",
            #  pode-se inserir o atributo checked na resposta selecionada,
            #  ficando esse bolinha selecionada quando o utilizador a ativa
            #  como answer.text tem o value do input, por exemplo numa pergunta com 3 opções:
            #  <input type="radio" name="resposta" value="1">
            #  <input type="radio" name="resposta" value="2">
            #  <input type="radio" name="resposta" value="3">
            # se answer.text="2", quer dizer q devemos por a de value="2" com checked.
            #  basta procurar no HTML por value="2" e adicionar o checked, ficando do tipo:
            #  <input type="radio" name="resposta" value="1">
            #  <input type="radio" name="resposta" value="2" checked>
            #  <input type="radio" name="resposta" value="3">

            # proposta de codigo:
            if question.type == "multipla":
                selectedInput = f'value="{answer.text}"'
                HTMLDaPergunta.replace(selectedInput, selectedInput + " checked")

        return HTMLDaPergunta

def proximaPergunta(testID, questionID):
    # deve existir uma lista dos ids das perguntas de cada teste
    # com base na ultima pergunta feita e no teste,
    # esta função deve identificar qual o id a proxima pergunta

    # isto pode estar num ficheiro
    sequenciaDeQuestionIDPorTeste = {
        1:[1,2],
    }

    if questionID == 0:
        return sequenciaDeQuestionIDPorTeste[testID][0]

    else:
        i = sequenciaDeQuestionIDPorTeste[testID].index(questionID)
        if i == len(sequenciaDeQuestionIDPorTeste[testID]) -1:
            # foi a ultima pergunta do teste
            return -1
        else:
            return sequenciaDeQuestionIDPorTeste[testID][i+1]