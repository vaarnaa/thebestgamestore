from django.shortcuts import render

# Create your views here.
def productview(request, product_id):
    """
    Write your view implementations for exercise 4 here.
    Remove the current return line below.
    """
    gameUrl = http://webcourse.cs.hut.fi / example_game.html
    return render(request, 'gameService/gameService.html', {'gameUrl': gameUrl})

