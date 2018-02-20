from .models import User, Player, Developer
from django.shortcuts import redirect
from social_core.pipeline.partial import partial
from .views import get_user_type

def create_player(backend, user, response, *args, **kwargs):
    user.is_player = True
    user.save()
    player = Player.objects.filter(user=user)
    if not player:
        Player.objects.create(user=user)


# partial says "we may interrupt, but we will come back here again"
@partial
def collect_user_type(strategy, request, backend, details, user=None, is_new=False, *args, **kwargs):
    # session 'local_password' is set by the pipeline infrastructure
    # because it exists in FIELDS_STORED_IN_SESSION
    user_type = strategy.session_get('user_type', None)
    request.session['backend_name'] = backend.name
    if user_type != 'player': #is_new and not 
        # if we return something besides a dict or None, then that is
        # returned to the user -- in this case we will redirect to a
        # view that can be used to get a password
        #return redirect('/signup/select_user_type')
        return redirect(get_user_type)

    # grab the user object from the database (remember that they may
    # not be logged in yet) and set their password.  (Assumes that the
    # email address was captured in an earlier step.)
    elif user and user_type == 'player':
        user.is_player = True
        user.save()
        player = Player.objects.filter(user=user)
        if not player:
            Player.objects.create(user=user)

    elif user and user_type == 'developer':
        user.is_developer = True
        user.save()
        developer = Developer.objects.filter(user=user)
        if not player:
            Developer.objects.create(user=user)

    # continue the pipeline
    return
