from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.core.validators import MinValueValidator
from decimal import *


class User(AbstractUser):
    is_player = models.BooleanField(default=False) #true if linked to player account
    is_developer = models.BooleanField(default=False) #true if linked to developer account
    is_social = models.BooleanField(default=False) #true if created by Google Sign In
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )


# Create your models here.
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


class Game(models.Model):

    category = models.ForeignKey(Category, related_name='games', on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    price =  models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to='games/%Y/%m/%d', blank=True)
    description = models.TextField()
    times_bought = models.PositiveIntegerField(default=0)

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






class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game)

    def get_id(self):
        return self.user.id

    def username(self):
        return self.user.get_username()

    def name(self):
        return self.user.get_full_name()

#* Developer: name, email, password, games
class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game)

    def get_id(self):
        return self.user.id

    def username(self):
        return self.user.get_username()

    def name(self):
        return self.user.get_full_name()


class Highscore(models.Model):
    DEFAULT_PK = 1
    game = models.ForeignKey(Game,
                             related_name='highscores',
                             on_delete=models.CASCADE)
    player = models.ForeignKey(Player,
                               related_name='highscores',
                               null=True,
                               on_delete=models.SET_NULL)
    score = models.IntegerField(default=0)

    def player_name(self):
        return self.player.username()

    class Meta:
        ordering = ('-score',)



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

    def get_total_cost(self):
        amount = sum(item.get_cost() for item in self.items.all())
        return amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order,
                              null=True,
                              on_delete=models.CASCADE)
