from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from .forms import PlayerSignUpForm, DeveloperSignUpForm, AddGameForm, SelectUserTypeForm, PriceUpdateForm
from .models import User, Game, Category, Player, Developer, Order
from django.shortcuts import get_object_or_404
from cart.forms import CartAddGameForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

"""
View for the third party signup. Renders te view where the user
selects the user type they want to create.
"""
def get_user_type(request):
    if request.method == 'POST':
        form = SelectUserTypeForm(request.POST)
        if form.is_valid():

            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            data = form.cleaned_data['select']
            request.session['user_type'] = data
            backend = request.session['backend_name']

            # once we have the user_type stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            return redirect('social:complete', backend=backend)
    else:
        form = SelectUserTypeForm()
    return render(request, "usertype_form.html", {'form': form})



"""
Renders the view after a new player has submitted the signup form.
"""
def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send the confirmation link to the new player.
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



"""
Renders the front page view after the new player has pressed their
activation link.
"""
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
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('core:index')
    else:
        return HttpResponse('Activation link is invalid!')



"""
Renders the view after a new developer has submitted the signup form.
"""
def developer_signup(request):
    if request.method == 'POST':
        form = DeveloperSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send the confirmation link to the new developer.
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

    else:
        form = DeveloperSignUpForm()
    return render(request, 'developer_signup.html', {'form': form})



"""
Renders the front page view after the new developer has pressed their
activation link.
"""
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
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('core:index')
    else:
        return HttpResponse('Activation link is invalid!')


"""
Renders the view with the details of the selected game.
"""

def game_detail(request, id, slug):
    if request.POST:
        return update_price(request)
    else:
        game = get_object_or_404(Game, id=id, slug=slug)
        cart_game_form = CartAddGameForm()
        the_user = request.user


        # Different view for player.
        if the_user.is_authenticated and the_user.is_player:
            player = get_object_or_404(Player, user_id=the_user.id)
            games = player.games.all()

            if game in games:   #Checking if the user owns the game in question.
                return render(request,
                            'game/detail_owned.html',
                            {'game': game})
            else:
                return render(request,
                            'game/detail.html',
                            {'game': game,
                            'cart_game_form': cart_game_form})
        # Different view for developer.
        elif the_user.is_authenticated and the_user.is_developer:
            dev = get_object_or_404(Developer, user_id=the_user.id)
            games = dev.games.all()
            form = PriceUpdateForm()
            if game in games:   #Checking if the user owns the game in question.
                times = []
                orders = Order.objects.filter(paid=True)
                for order in orders:
                    for item in order.items.all():
                        if item.game == game:
                            times.append((order.updated, item.price))




                return render(request,
                            'game/detail_dev.html',
                            {'game': game,
                             'form': form,
                             'times': times})
            else:
                return render(request,
                            'game/detail.html',
                            {'game': game,
                            'cart_game_form': cart_game_form})
        # Different view if the user is not authenticated.
        else:
            return render(request,
                        'game/detail.html',
                        {'game': game,
                        'cart_game_form': cart_game_form})



"""
Renders the front page of the webshop. Lists all available games under their categories.
"""
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



"""
Renders the view for "My games" -page. Lists the games owned.
"""
def games(request):
    uid = request.user.id
    games = None
    # Different view for player.
    if request.user.is_authenticated and request.user.is_player:
        player = get_object_or_404(Player, user_id=uid)
        games = player.games.all()
        return render(request, 'games.html', {'games': games})
    # Different view for developer.
    elif request.user.is_authenticated and request.user.is_developer:
        dev = get_object_or_404(Developer, user_id=uid)
        games = dev.games.all()
        return render(request, 'games.html', {'games': games})
    # Redirects to frontpage.
    else:
        return redirect('core:index')

"""
Renders the "add game" -page for developers.
"""
def add_games(request):
    if request.user.is_authenticated and request.user.is_developer:
        form = AddGameForm()
        return render(request, 'add_games.html', {'form': form })
    else:
        return redirect('core:index')

"""
Adds a new game on the webshop, and renders a confirmation view.
"""
def add_game(request):
    if request.user.is_authenticated and request.user.is_developer:
        if request.method == 'POST':
            # Creates a slug for the new game.
            slugger = request.POST['name'].lower().replace(' ', '-').replace('ä', 'a').replace('ö', 'o')

            # If a game with the same slug exists, adds a number after it to make it unique.
            if Game.objects.filter(slug=slugger):
                i = 1
                slugger = slugger  + str(i)
                while Game.objects.filter(slug=slugger):
                    i += 1
                    slugger = slugger[:-1]  + str(i)

            img = 'no_image.png'   # Default image if no image is given.
            if request.POST.get('image',False):
                img = request.POST['image']
            price = 0
            if float(request.POST['price']) > 0:    # Price cannot be less than 0.
                price = request.POST['price']
            # Adds the new game to database.
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
    else:
        return redirect('core:index')

"""
Removes the game in question.
"""
def remove_game(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_developer:
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
            return redirect('core:index')
    else:
        return redirect('core:index')

"""
Updates the price of the given game.
"""
def update_price(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_developer:
        id = request.POST['id']
        game = get_object_or_404(Game, id=id)
        uid = request.user.id
        dev = get_object_or_404(Developer, user_id=uid)
        games = dev.games.all()
        form = PriceUpdateForm()
        if game in games:
            game.price = request.POST['new_price']
            game.save()
            times = []
            orders = Order.objects.filter(paid=True)
            for order in orders:
                for item in order.items.all():
                    if item.game == game:
                        times.append((order.updated, item.price))
            return render(request,
                        'game/detail_dev.html',
                        {'game': game,
                         'form': form,
                         'times': times})
        else:
            return redirect('core:index')
    else:
        return redirect('core:index')

"""
Renders the view for global highscores.
"""
def highscores(request):
    games = Game.objects.all()
    scores = []
    for game in games:
        if game.highscores.all():
            s = game.highscores.all().order_by("-score")
            scores.append(game)
    return render(request, 'highscores.html', {'scores': scores})

"""
Renders the view for players own highscores.
"""
def player_highscores(request):
    player = get_object_or_404(Player, user_id=request.user.id)
    scores = player.highscores.all()

    return render (request, 'player_highscores.html', {"scores": scores})


"""
Renders the view for signup page.
"""
def signup(request):
    return render(request, 'signup.html')


"""
Render the view for login page.
"""
def login(request):
    return render(request, 'login.html')
