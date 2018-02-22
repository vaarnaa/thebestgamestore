from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Game
from .cart import Cart
from .forms import CartAddGameForm

"""
Adds a game to the shopping cart.
"""
@require_POST
def cart_add(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(Game, id=game_id)
    form = CartAddGameForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(game=game,
                 quantity=1,
                 update_quantity=True)
    return redirect('cart:cart_detail')

"""
Removes a game from the shopping cart.
"""
def cart_remove(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(Game, id=game_id)
    cart.remove(game)
    return redirect('cart:cart_detail')

"""
Lists the games in the shopping cart.
"""
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddGameForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
