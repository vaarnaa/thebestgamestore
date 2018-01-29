from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Game(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    image = models.ImageField()
    description = models.TextField()

#* Player: name, email, password, games

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

#* Highscore: gameName, playerName, score
