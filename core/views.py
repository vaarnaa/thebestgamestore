from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.views.generic import CreateView
from .forms import PlayerSignUpForm, DeveloperSignUpForm, AddGameForm, SelectUserTypeForm, PriceUpdateForm
from .models import User, Game, Category, Player, Developer, Highscore
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from cart.forms import CartAddGameForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.urls import reverse


def get_user_type(request):
    if request.method == 'POST':
        form = SelectUserTypeForm(request.POST)
        if form.is_valid():
            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            request.session['user_type'] = 'player'#form.cleaned_data['select']
            #backend = current_partial.backend
            # once we have the password stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            #return redirect(reverse('oauth/complete/google-oauth2/')) google-auth2
            #return redirect(reverse('social:complete', args=("backend_name,")))
            backend = request.session['backend_name']
            return redirect('social:complete', backend=backend)
            #return redirect(reverse('social:complete', args=("google-auth2,")))
            #return redirect(reverse('/oauth/complete/google-oauth2/'))
            #return redirect('/oauth/complete/google-auth2')
    else:
        form = SelectUserTypeForm()
    return render(request, "usertype_form.html", {'form': form})


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
    the_user = request.user
    if the_user.is_authenticated and the_user.is_player:
        player = get_object_or_404(Player, user_id=the_user.id)
        games = player.games.all()
        if game in games:
            return render(request,
                        'game/detail_owned.html',
                        {'game': game})
        else:
            return render(request,
                        'game/detail.html',
                        {'game': game,
                        'cart_game_form': cart_game_form})

    elif the_user.is_authenticated and the_user.is_developer:
        dev = get_object_or_404(Developer, user_id=the_user.id)
        games = dev.games.all()
        form = PriceUpdateForm()
        if game in games:
            return render(request,
                        'game/detail_dev.html',
                        {'game': game,
                         'form': form})
        else:
            return render(request,
                        'game/detail.html',
                        {'game': game,
                        'cart_game_form': cart_game_form})

    else:
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
    uid = request.user.id
    games = None
    if request.user.is_player:
        player = get_object_or_404(Player, user_id=uid)
        games = player.games.all()
    elif request.user.is_developer:
        dev = get_object_or_404(Developer, user_id=uid)
        games = dev.games.all()
    return render(request, 'games.html', {'games': games})


def add_games(request):
    form = AddGameForm()
    return render(request, 'add_games.html', {'form': form })




def add_game(request):
    if request.method == 'POST':
        slugger = request.POST['name'].lower().replace(' ', '-').replace('ä', 'a').replace('ö', 'o')
        if Game.objects.filter(slug=slugger):
            i = 1
            slugger = slugger  + str(i)
            while Game.objects.filter(slug=slugger):
                i += 1
                slugger = slugger  + str(i)

        img = 'no_image.png'
        if request.FILES.get('image',False):
            img = request.FILES['image']
        price = 0
        if float(request.POST['price']) > 0:
            price = request.POST['price']
        game = Game.objects.create(category=get_object_or_404(Category, id=request.POST['category']),
                            url=request.POST['url'],
                            name=request.POST['name'],
                            slug=slugger,
                            price=price,
                            image=img,
                            description=request.POST['description'])
        dev = get_object_or_404(Developer, user_id=request.user.id)
        dev.games.add(game)
        dev.save()
    return render(request, 'game/added.html', {'game': game})


def remove_game(request):
    id = request.POST['id']
    game = get_object_or_404(Game, id=id)
    uid = request.user.id
    dev = get_object_or_404(Developer, user_id=uid)
    games = dev.games.all()
    if game in games:
        name = game.name
        game.delete(keep_parents=True)
        return render(request, 'game/removed.html', {'game_name': name})
    else:
        return render(request, 'index.html')


def update_price(request):
    id = request.POST['id']
    game = get_object_or_404(Game, id=id)
    uid = request.user.id
    dev = get_object_or_404(Developer, user_id=uid)
    games = dev.games.all()
    form = PriceUpdateForm()
    if game in games:
        game.price = request.POST['new_price']
        game.save()
        return render(request,
                    'game/detail_dev.html',
                    {'game': game,
                     'form': form})
    else:
        return render(request, 'index.html')


def highscores(request):
    games = Game.objects.all()
    scores = []
    for game in games:
        if game.highscores.all():
            s = game.highscores.all().order_by("-score")
            scores.append(game)
    return render(request, 'highscores.html', {'scores': scores})

def player_highscores(request):
    player = get_object_or_404(Player, user_id=request.user.id)
    scores = player.highscores.all()

    return render (request, 'player_highscores.html', {"scores": scores})

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')
