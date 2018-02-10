from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

from core.models import Game, Player
# Create your views here.
def game(request, game_id):
    
    player = get_object_or_404(Player, get_id=request.user.id)
    game = get_object_or_404(Game, id=game_id)
    gameUrl = game.url

    return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl})






























def savescore(request, game_id):
    
    player = get_object_or_404(Player, get_id=player_id)
    game = get_object_or_404(Game, id=game_id)
    gameUrl = game.url

    return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl})

def savegame(request, game_id):
    
    player = get_object_or_404(Player, get_id=player_id)
    game = get_object_or_404(Game, id=game_id)
    gameUrl = game.url

    return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl})

def loadgame(request, game_id):
    
    player = get_object_or_404(Player, get_id=player_id)
    game = get_object_or_404(Game, id=game_id)
    gameUrl = game.url

    return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl})

