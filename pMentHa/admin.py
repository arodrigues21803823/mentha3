from django.contrib import admin
from .models import Advisor, Patient, Report, Test, Question, Answer

# Register your models here.
admin.site.register(Advisor)
admin.site.register(Patient)
admin.site.register(Report)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)

