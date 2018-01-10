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

#* Developer: name, email, password, games
#* Player: name, email, password, games

#* Highscore: gameName, playerName, score
