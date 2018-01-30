from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from core.models import Game, Player

def add_game(request, d_id, game_id):
    developer = get_object_or_404(Developer, get_id=d_id)
    game = get_object_or_404(Game, id=game_id)

    developer.games.add(game)


    #return something

def create_developer(request, user_id):
    current_user = get_object_or_404(User, id=user_id)

    d = Developer(user = current_user)




    #return something
