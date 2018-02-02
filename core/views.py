from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Greeting
from django.contrib.auth import login as auth_login, authenticate
from django.views.generic import CreateView
from .forms import PlayerSignUpForm, DeveloperSignUpForm
from .models import User, Game, Category, Player, Developer
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from cart.forms import CartAddGameForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('player_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            response = HttpResponse()
            response.write("<p style=\"text-align:center; padding-top:40px\">An email has been sent to " + to_email + "</p>")
            response.write("<p style=\"text-align:center\">Please confirm your email address to complete the registration.</p>")
            return response

    else:
        form = PlayerSignUpForm()
    return render(request, 'player_signup.html', {'form': form})


def player_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_player = True
        user.save()
        player = Player.objects.create(user=user)
        auth_login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


def developer_signup(request):
    if request.method == 'POST':
        form = DeveloperSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('developer_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            response = HttpResponse()
            response.write("<p style=\"text-align:center; padding-top:40px\">An email has been sent to " + to_email + "</p>")
            response.write("<p style=\"text-align:center\">Please confirm your email address to complete the registration.</p>")
            return response
            #return HttpResponse('An email has been sent to', to-email Please confirm your email address to complete the registration')
    else:
        form = DeveloperSignUpForm()
    return render(request, 'developer_signup.html', {'form': form})


def developer_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_developer = True
        user.save()
        developer = Developer.objects.create(user=user)
        auth_login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

"""class PlayerSignUp(CreateView):
    model = User
    form_class = PlayerSignUpForm
    template_name = 'player_signup.html'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('/')"""

"""class DeveloperSignUp(CreateView):
    model = User
    form_class = DeveloperSignUpForm
    template_name = 'developer_signup.html'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect('/')"""




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
