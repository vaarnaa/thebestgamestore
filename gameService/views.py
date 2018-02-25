from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from cart.forms import CartAddGameForm
from django.urls import reverse
from core.models import Game, Player, Highscore, Gamestate
from core.views import highscores
import json

# Create your views here.
def play(request, id):

    player = get_object_or_404(Player, user_id=request.user.id)
    game = get_object_or_404(Game, id=id)

    if request.POST:
        if game in player.games.all():
            gameUrl = str(game.url)
            if request.POST['messageType'] == 'SAVE':
                old_gamestates = Gamestate.objects.filter(game=stateGame, player=statePlayer)
                for state in old_gamestates:
                    state.delete(keep_parents=True)

                gamestate = request.POST['gameState']

                Gamestate.objects.create(stateGame=game,
                                             statePlayer=player,
                                             gamestate=gamestate)


                return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl,
                                                                        'game': game})

            elif request.POST['messageType'] == 'LOAD_REQUEST':
                pass

            

        cart_game_form = CartAddGameForm()
        return render(request, 'game/detail.html', {'game': game,
                                                    'cart_game_form': cart_game_form})

    else:
        if game in player.games.all():
            gameUrl = str(game.url)

            return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl,
                                                                    'game': game})
        else:
            cart_game_form = CartAddGameForm()
            return render(request, 'game/detail.html', {'game': game,
                                                        'cart_game_form': cart_game_form})


def savescore(request, id):

    player = get_object_or_404(Player, user_id=request.user.id)
    game = get_object_or_404(Game, id=id)
    player_score = player.highscores.filter(game=game)
    new_score = int(request.POST['score'])
    if player_score:
        if player_score[0].score < new_score:
            player_score[0].score = new_score
            player_score[0].player = player
            player_score[0].save()
    else:
        Highscore.objects.create(game=game,
                                 player=player,
                                 score=new_score)

    return redirect(reverse('highscores'), permanent=True)


def savegame(request, id):

    player = get_object_or_404(Player, user_id=request.user.id)
    game = get_object_or_404(Game, id=id)
    gamestate = request.POST['gameState']
    Gamestate.objects.create(stateGame=game,
                                 statePlayer=player,
                                 gamestate=gamestate)


    return redirect('gameService:play', {'id': id})



def loadgame(request, game_id):

    player = get_object_or_404(Player, get_id=player_id)
    game = get_object_or_404(Game, id=game_id)
    gameUrl = game.url

    return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl})
