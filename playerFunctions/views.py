from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from core.models import Game, Player

def add_game(request, player_id, game_id):
    player = get_object_or_404(Player, get_id=player_id)
    game = get_object_or_404(Game, id=game_id)

    player.games.add(game)



    #return something

def create_player(request, user_id):
    current_user = get_object_or_404(User, id=user_id)

    p = Player(user = current_user)




    #return something
