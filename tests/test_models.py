from django.test import TestCase
from django.utils import timezone
from decimal import *

from core.models import User, Player, Developer, Game, Category, Highscore, Order, OrderItem


class UserTypeModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user_player = User.objects.create_user(username='Matti1', email='matti1.meikalainen1@gmail.com', password='salasana1', first_name='Matti1', last_name='Meikalainen1')
        user_player.is_player = True
        user_player.save()
        Player.objects.create(user=user_player)

        user_developer = User.objects.create_user(username='Matti2', email='matti2.meikalainen2@gmail.com', password='salasana2', first_name='Matti2', last_name='Meikalainen2')
        user_developer.is_player = True
        user_developer.save()
        Developer.objects.create(user=user_developer)

    def test_labels(self):
        player_user = User.objects.get(id=1)
        player = player_user.player
        field_label_player = player_user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label_player,'first name')
        field_label_player = player_user._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label_player,'last name')
        field_label_player = player_user._meta.get_field('username').verbose_name
        self.assertEquals(field_label_player,'username')
        field_label_player = player_user._meta.get_field('email').verbose_name
        self.assertEquals(field_label_player,'email address')
        field_label_player = player_user._meta.get_field('password').verbose_name
        self.assertEquals(field_label_player,'password')

        developer_user = User.objects.get(id=2)
        developer = developer_user.developer
        field_label_developer = developer_user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label_developer,'first name')
        field_label_developer = developer_user._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label_developer,'last name')
        field_label_developer = developer_user._meta.get_field('username').verbose_name
        self.assertEquals(field_label_developer,'username')
        field_label_developer = developer_user._meta.get_field('email').verbose_name
        self.assertEquals(field_label_developer,'email address')
        field_label_developer = developer_user._meta.get_field('password').verbose_name
        self.assertEquals(field_label_developer,'password')

    def test_email_max_length(self):
        player_user = User.objects.get(id=1)
        player = player_user.player
        max_length = player_user._meta.get_field('email').max_length
        self.assertEquals(max_length,255)

        developer_user = User.objects.get(id=2)
        developer = developer_user.developer
        max_length = developer_user._meta.get_field('email').max_length
        self.assertEquals(max_length,255)

    def test_custom_methods(self):
        player_user = User.objects.get(id=1)
        player = player_user.player
        player_id = player.get_id()
        self.assertEquals(player_id, player_user.id)
        player_username = player.username()
        self.assertEquals(player_username, player_user.username)
        player_name = player.name()
        self.assertEquals(player_name, player_user.first_name + " " + player_user.last_name)

        developer_user = User.objects.get(id=2)
        developer = developer_user.developer
        developer_id = developer.get_id()
        self.assertEquals(developer_id, developer_user.id)
        developer_username = developer.username()
        self.assertEquals(developer_username, developer_user.username)
        developer_name = developer.name()
        self.assertEquals(developer_name, developer_user.first_name + " " + developer_user.last_name)



class CategoryModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="RPG", slug="rpg")
        Category.objects.create(name="Action", slug="action")

    def test_max_field_lengths(self):
        category= Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length,200)
        max_length = category._meta.get_field('slug').max_length
        self.assertEquals(max_length,200)

    def test_meta_fields(self):
        category= Category.objects.get(id=1)
        category_label = category._meta.verbose_name
        self.assertEquals(category_label,'category')
        category_label = category._meta.verbose_name_plural
        self.assertEquals(category_label,'categories')
        category_first = Category.objects.filter().first()
        self.assertEquals(category_first.name, 'Action')

    def test_custom_methods(self):
        category= Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEquals(expected_object_name,str(category))
        self.assertEquals(category.get_absolute_url(),'/rpg/')


class GameModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        category = Category.objects.create(name="Action", slug="action")
        Game.objects.create(
            category = category,
            url = 'http://127.0.0.1:8000/static/own_game.html',
            name = 'WormGame',
            slug = "wormgame",
            price = "100.50",
            image = "http://127.0.0.1:8000/static/img/123369.png",
            description = 'Matopeli',
            times_bought = '1')

        Game.objects.create(
            category = category,
            url = 'http://127.0.0.1:8000/static/own_game.html',
            name = 'ActionGame',
            slug = "actiongame",
            price = "100.50",
            image = "http://127.0.0.1:8000/static/img/123369.png",
            description = 'Action-peli',
            times_bought = '1')


    def test_game_fields(self):
        game = Game.objects.get(id=1)
        name_max_length = game._meta.get_field('name').max_length
        self.assertEquals(name_max_length,255)
        slug_max_length = game._meta.get_field('slug').max_length
        self.assertEquals(slug_max_length,255)
        price_max_digits = game._meta.get_field('price').max_digits
        self.assertEquals(price_max_digits, 10)
        decimals = game._meta.get_field('price').decimal_places
        self.assertEquals(decimals, 2)

    def test_meta_fields(self):
        category = Category.objects.get(id=1)
        games = category.games.all()
        game1 = games[0]
        game2 = games[1]
        self.assertTrue(game1.category, category)
        self.assertTrue(game2.category, category)

        game_label = game1._meta.verbose_name
        self.assertEquals(game_label,'game')

        game_label = game1._meta.verbose_name_plural
        self.assertEquals(game_label,'games')

        game_first = Game.objects.filter().first()
        self.assertEquals(game_first.name, 'ActionGame')


    def test_custom_methods(self):
        game = Game.objects.get(id=1)
        expected_object_name = game.name
        self.assertEquals(expected_object_name,str(game))
        self.assertEquals(game.get_absolute_url(),'/1/wormgame/')
        self.assertEquals(game.get_short_description(), 'Matopeli')



class HighscoreModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Action", slug="action")
        game = Game.objects.create(
            category = category,
            url = 'http://127.0.0.1:8000/static/own_game.html',
            name = 'WormGame',
            slug = "wormgame",
            price = "100.50",
            image = "http://127.0.0.1:8000/static/img/123369.png",
            description = 'Matopeli',
            times_bought = '1')
        user_player = User.objects.create_user(username='Matti1', email='matti1.meikalainen1@gmail.com', password='salasana1', first_name='Matti1', last_name='Meikalainen1')
        user_player.is_player = True
        user_player.save()
        player = Player.objects.create(user=user_player)
        Highscore.objects.create(game=game, player=player, score=10)
        Highscore.objects.create(game=game, player=player, score=100)


    def test_highscore_fields(self):
        player_user = User.objects.get(id=1)
        player = player_user.player
        game = Game.objects.get(id=1)
        highscore1 = game.highscores.filter().first()
        highscore2 = player.highscores.filter().first()
        self.assertTrue(highscore1, highscore2)


    def test_custom_methods(self):
        player_user = User.objects.get(id=1)
        game = Game.objects.get(id=1)
        highscore1 = game.highscores.filter().first()
        expected_object_name = highscore1.player_name()
        self.assertEquals(expected_object_name,player_user.username)

        highscore_first = Highscore.objects.filter().first()
        self.assertEquals(highscore_first.score, 100)


class OrderItemModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Action", slug="action")
        game = Game.objects.create(
            category = category,
            url = 'http://127.0.0.1:8000/static/own_game.html',
            name = 'WormGame',
            slug = "wormgame",
            price = "100.50",
            image = "http://127.0.0.1:8000/static/img/123369.png",
            description = 'Matopeli',
            times_bought = '1')

        order = Order.objects.create(
            first_name = 'Matti',
            last_name = 'Meikalainen',
            email = 'matti.meikalainen@gmail.com',
            address = 'Otakaari 1',
            postal_code = '00800',
            city = 'Espoo',
            created = timezone.now(),
            updated = timezone.now(),
            paid = True)

        OrderItem.objects.create(order=order, game=game, price=10.10, quantity=3)

    def test_model_fields(self):
        order = Order.objects.get(id=1)
        game = Game.objects.get(id=1)
        orderItem1 = order.items.all().first()
        orderItem2 = game.order_items.all().first()
        self.assertEquals(orderItem1, orderItem2)

        price_max_digits = orderItem1._meta.get_field('price').max_digits
        self.assertEquals(price_max_digits,10)

        price_decimals = orderItem1._meta.get_field('price').decimal_places
        self.assertEquals(price_decimals,2)

        expected_object_name = '1'
        self.assertEquals(expected_object_name, str(orderItem1))

        expected_value = Decimal('30.30')
        self.assertEquals(expected_value, orderItem1.get_cost())


class OrderModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Action", slug="action")
        game = Game.objects.create(
            category = category,
            url = 'http://127.0.0.1:8000/static/own_game.html',
            name = 'WormGame',
            slug = "wormgame",
            price = "100.50",
            image = "http://127.0.0.1:8000/static/img/123369.png",
            description = 'Matopeli',
            times_bought = '1')

        order = Order.objects.create(
            first_name = 'Matti1',
            last_name = 'Meikalainen1',
            email = 'matti1.meikalainen1@gmail.com',
            address = 'Otakaari 1',
            postal_code = '00800',
            city = 'Espoo',
            created = timezone.now(),
            updated = timezone.now(),
            paid = True)

        Order.objects.create(
            first_name = 'Matti2',
            last_name = 'Meikalainen2',
            email = 'matti2.meikalainen2@gmail.com',
            address = 'Otakaari 1',
            postal_code = '00800',
            city = 'Espoo',
            created = timezone.now(),
            updated = timezone.now(),
            paid = True)

        OrderItem.objects.create(order=order, game=game, price=10.00, quantity=4)
        OrderItem.objects.create(order=order, game=game, price=20.0, quantity=3)

    def test_order_fields(self):
        order = Order.objects.get(id=1)
        first_name_max_length = order._meta.get_field('first_name').max_length
        self.assertEquals(first_name_max_length,50)
        last_name_max_length = order._meta.get_field('last_name').max_length
        self.assertEquals(last_name_max_length,50)
        address_max_length = order._meta.get_field('address').max_length
        self.assertEquals(address_max_length,250)
        postal_code_max_length = order._meta.get_field('postal_code').max_length
        self.assertEquals(postal_code_max_length,20)
        city_max_length = order._meta.get_field('city').max_length
        self.assertEquals(city_max_length,100)

    def test_custom_methods(self):
        order1 = Order.objects.get(id=1)
        order2 = Order.objects.get(id=2)

        expected_object_name ='Order 1'
        self.assertEquals(expected_object_name, str(order1))

        order_first = Order.objects.filter().first()
        self.assertTrue(order_first == order2)

        expected_order_cost = Decimal('100')
        self.assertTrue(expected_order_cost == order1.get_total_cost())
