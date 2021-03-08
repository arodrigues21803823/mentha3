from django.db import models


# Create your models here.
class Question(models.Model):
    classes = models.CharField(max_length=64)
    statement = models.TextField(max_length=258)
    quotation = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}:{self.statement}"


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
    scale = models.CharField(max_length=64)
    quotation = models.CharField(max_length=64)
    question = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True, related_name="respostas")
    #test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True, related_name="test")

    def __str__(self):
        return f"{self.text}"


class Advisor(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=254)

    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    tests = models.ManyToManyField('Test', blank=True, related_name="tests")

    def __str__(self):
        return f"{self.name}"


class Report(models.Model):
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True)
    advisor = models.ForeignKey('Advisor', on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"Relatório do teste {self.test}: {self.text}"
