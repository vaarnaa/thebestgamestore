from django.shortcuts import render
from django.http import HttpResponse
from .models import Greeting
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import PlayerSignUpForm, DeveloperSignUpForm
from .models import User, Game, Category
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from cart.forms import CartAddGameForm

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




def game_detail(request, id, slug):
    game = get_object_or_404(Game, id=id, slug=slug)
    cart_game_form = CartAddGameForm()
    return render(request,
                  'game/detail.html',
                  {'game': game,
                   'cart_game_form': cart_game_form})



# Create your views here.
def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    games = Game.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        games = games.filter(category=category)
    return render(request, 'index.html', {'category': category,
                                                      'categories': categories,
                                                      'games': games})


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
