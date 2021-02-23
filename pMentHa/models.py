from django.db import models


# Create your models here.
class Question(models.Model):
    classes = models.CharField(max_length=64)
    statement = models.TextField(max_length=258)
    result = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.classes} , {self.statement}"


class Test(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    statement = models.TextField(max_length=1000)
    questions = models.ManyToManyField('Question', blank=True, related_name="Questions")

    def __str__(self):
        return f"O teste {self.id}"


class Answer(models.Model):
    text = models.TextField(max_length=258)
    scale = models.CharField(max_length=64)
    quotation = models.CharField(max_length=64)
    question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}: {self.text} , {self.scale} , {self.quotation}, {self.test}, {self.question}"


class Advisor(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=254)
    test = models.ManyToManyField('Test', blank=True, related_name="test")

    def __str__(self):
        return f"{self.name}"


class Patient(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    tests = models.ManyToManyField('Test', blank=True, related_name="tests")

    def __str__(self):
        return f"{self.name} está inscrito nos testes {self.tests}"


class Report(models.Model):
    test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True)
    advisor = models.ForeignKey('Advisor', on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"Relatório do teste {self.test}: {self.patient}, {self.text}"
