from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Game(models.Model):
    #name = models.
    url = models.URLField()
    name = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    image = models.ImageField()
    description = models.TextField()

#* Player: name, email, password, games

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game)

    def get_id(self):
        return user.id

    def username(self):
        return user.username

#* Developer: name, email, password, games
class Developer(models.model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    games = models.ManyToManyField(Game)

    def get_id(self):
        return user.id

    def username(self):
        return user.username

#* Highscore: gameName, playerName, score
