from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def games(request):
    return render(request, 'games.html')

def highscores(request):
    return render(request, 'highscores.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
