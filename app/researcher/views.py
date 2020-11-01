from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse
from .models import User


# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def search_status(request):
    if request.POST:
        user = User.objects.get(id=request['id'])
        test_result = user.test_result
        return HttpResponse("User find")

    return HttpResponse("Invalid request")


def change_status(request):
    if request.POST:
        user = User.objects.get(id=request['id'])
        user.test_result = request['status']
        user.save()
        return HttpResponse("Status changed")

    return HttpResponse("Invalid request")


def delete_people(request):
    if request.POST:
        user = User.objects.get(id=request['id'])
        user.delete()
        return HttpResponse("User deleted")

    return HttpResponse("Invalid request")