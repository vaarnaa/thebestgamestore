from django.test import TestCase

# Create your tests here.

from core.models import User, Player, Developer, Game, Category


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

    def test_category_field(self):
        pass

    def test_meta_fields(self):
        category = Category.objects.get(id=1)
        game1 = Game.objects.get(id=1)
        game2 = Game.objects.get(id=2)
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
