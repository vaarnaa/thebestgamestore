from .models import Player

def create_player(backend, user, response, *args, **kwargs):
    user.is_player = True
    user.save()
    player = Player.objects.filter(user=user)
    if not player:
        Player.objects.create(user=user)
