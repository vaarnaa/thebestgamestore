from decimal import Decimal
from django.conf import settings
from core.models import Game


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the games from the database.
        """
        game_ids = self.cart.keys()
        # get the game objects and add them to the cart
        games = Game.objects.filter(id__in=game_ids)
        for game in games:
            self.cart[str(game.id)]['game'] = game

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, game, quantity=1, update_quantity=False):
        """
        Add a game to the cart or update its quantity.
        """
        game_id = str(game.id)
        if game_id not in self.cart:
            self.cart[game_id] = {'quantity': 0,
                                      'price': str(game.price)}
        if update_quantity:
            self.cart[game_id]['quantity'] = quantity
        else:
            self.cart[game_id]['quantity'] += quantity
        self.save()

    def remove(self, game):
        """
        Remove a game from the cart.
        """
        game_id = str(game.id)
        if game_id in self.cart:
            del self.cart[game_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        print(self.session[settings.CART_SESSION_ID])
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
