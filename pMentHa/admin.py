from django.contrib import admin
from .models import *

# Register your models here.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question','text')


class TestAdmin(admin.ModelAdmin):
    fields = ['name','questions','advisor','statement']
    list_display = ('name','get_questions')

    def get_questions(self, obj):
        return "\n".join([q.text for q in obj.questions.all()])

class OrderAdmin(admin.StackedInline):
    model = QuestionOrder

class QuestionOrderAdmin(admin.ModelAdmin):
    list_display = ("test","order","question")

class OptionsAdmin(admin.StackedInline):
    model = Option

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("multipla","text")

    inlines = [OrderAdmin,OptionsAdmin]

class ResolutionAdmin(admin.ModelAdmin):
    list_display = ("id","test","patient")

admin.site.register(Test, TestAdmin)
admin.site.register(Question,QuestionsAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Resolution,ResolutionAdmin)
admin.site.register(Option)
admin.site.register(QuestionOrder,QuestionOrderAdmin)
admin.site.register(Advisor)
admin.site.register(Patient)
admin.site.register(Report)


