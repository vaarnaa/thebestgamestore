from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import PlayerSignUpForm, DeveloperSignUpForm
from .models import User

class PlayerSignUp(CreateView):
    model = User
    form_class = PlayerSignUpForm
    template_name = 'player_signup.html'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('/')

class DeveloperSignUp(CreateView):
    model = User
    form_class = DeveloperSignUpForm
    template_name = 'developer_signup.html'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('/')



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
