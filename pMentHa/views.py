from django.shortcuts import render
from .models import Test


# Create your views here.
def index(request):
    return render(request, "pMentHa/index.html", {
        "pMentHa": Test.objects.all(),
    })


def test(request, test_id):
    test = Test.objects.get(pk=test_id)
    return render(request, "pMentHa/test.html", {
        "test": test,
        "name": test.name.all()
    })
