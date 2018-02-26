from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.core.validators import MinValueValidator
from decimal import *

"""
Model extendig Django's native User model.
Extra attributes is_player and is_developer, to make difference
between usertypes. No user shoul ever be both at the same time. Also has
the User classes optional email -field.
"""
class User(AbstractUser):
    is_player = models.BooleanField(default=False) #true if linked to player account
    is_developer = models.BooleanField(default=False) #true if linked to developer account
    is_social = models.BooleanField(default=False) #true if created by Google Sign In
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )


"""
Model for different game categories. Used to list the different games
under categories on the shop page.
"""
class Category(models.Model):
    DEFAULT_PK = 1
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:game_list_by_category', args=[self.slug])



"""
Model for the games sold and played on the website.
Games can have many players as well as players may have mane games.
Games can only have one Developer, the one who added it on the website.
"""
class Game(models.Model):

    category = models.ForeignKey(Category, related_name='games', on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    price =  models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to='games/%Y/%m/%d', blank=True)
    description = models.TextField()
    times_bought = models.PositiveIntegerField(default=0)

    """
    Function to get a shortened version of the description that can
    fit smaller text elements.
    """
    def get_short_description(self):
        length = len(self.description)
        if (length > 100):
            short = self.description[:80] + "..."
            return short
        else:
            return self.description



    class Meta:
        ordering = ('name',)
        #index_together = (('id', 'slug'),)
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:game_detail', args=[self.id, self.slug])


"""
Model for the player users on the website. Attributes include as
primary key, the user, and as many to many relation the games
owned by the player.
"""
class Player(models.Model):
    user = models.OneToOneField(User, related_name="player", on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game)

    def get_id(self):
        return self.user.id

    def username(self):
        return self.user.get_username()

    def name(self):
        return self.user.get_full_name()


"""
Mode for the developers on the website. Attributes include as
primary key, the user, and as many to many relation the games
added by the developer."""
class Developer(models.Model):
    user = models.OneToOneField(User, related_name="developer", on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game)

    def get_id(self):
        return self.user.id

    def username(self):
        return self.user.get_username()

    def name(self):
        return self.user.get_full_name()


"""
Model for storing the highscores on the website. Attributes include
the game the score is referenced to, the player who made the score
and the score value. Model instances are used to show the views for
personal and global highscore tables.
"""
class Highscore(models.Model):
    DEFAULT_PK = 1
    game = models.ForeignKey(Game,
                             related_name='highscores',
                             on_delete=models.CASCADE)
    player = models.ForeignKey(Player,
                               related_name='highscores',
                               null=True,
                               on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def player_name(self):
        return self.player.username()

    class Meta:
        ordering = ('-score',)



"""
Model used to store gamestates of different games for different players.
Used to load a previous state when playing the game.
"""
class Gamestate(models.Model):
    DEFAULT_PK = 1
    stateGame = models.ForeignKey(Game,
                             related_name='gamestate',
                             on_delete=models.SET_NULL,
                             null=True)
    statePlayer = models.ForeignKey(Player,
                               related_name='gamestate',
                               null=True,
                               on_delete=models.SET_NULL)
    gamestate = models.TextField(default="")
    time = models.DateTimeField(default=datetime.now())

    def player_name(self):
        return self.player.username()


"""
Model for the orders on the websites. The order holds the billing
information and the payment status, as well as the order items
of the order. Has a function to calculate the total price of the
order.
"""
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    """
    Fuction to calculate the total price of the order.
    """
    def get_total_cost(self):
        amount = sum(item.get_cost() for item in self.items.all())
        return amount


"""
Model for different order item included in the order.
"""
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

"""
Model for holding the payment id during third party payment site visit.
"""
class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order,
                              null=True,
                              on_delete=models.CASCADE)
